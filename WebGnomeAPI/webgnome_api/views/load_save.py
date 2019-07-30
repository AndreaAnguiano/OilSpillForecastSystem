"""
Views for the model load/save operations.
"""
import os
import logging
import tempfile
from threading import current_thread

from pyramid.view import view_config
from pyramid.response import Response, FileIter
from pyramid.httpexceptions import (HTTPBadRequest,
                                    HTTPNotFound)

from cornice import Service

from gnome.persist import is_savezip_valid
from gnome.model import Model

from ..common.helpers import update_savefile
from ..common.system_resources import list_files
from ..common.common_object import (RegisterObject,
                                    clean_session_dir,
                                    get_persistent_dir)
from ..common.session_management import (init_session_objects,
                                         set_active_model,
                                         get_active_model,
                                         acquire_session_lock)
from ..common.views import (can_persist,
                            cors_response,
                            cors_exception,
                            cors_policy,
                            process_upload,
                            activate_uploaded)
from webgnome_api.common.session_management import get_session_objects

log = logging.getLogger(__name__)


persisted_files_api = Service(name='uploaded', path='/uploaded',
                              description="Persistent Uploaded Files API",
                              cors_policy=cors_policy)


@view_config(route_name='upload', request_method='OPTIONS')
def upload_model_options(request):
    return cors_response(request, request.response)


@view_config(route_name='upload', request_method='POST')
def upload_model(request):
    '''
        Uploads a new model in the form of a zipfile and registers it as the
        current active model.

        We are generating our own filename instead of trusting
        the incoming filename since that might result in insecure paths.

        We may want to eventually use something other than /tmp,
        and if you write to an untrusted location you will need to do
        some extra work to prevent symlink attacks.
    '''
    clean_session_dir(request)
    file_path, _name = process_upload(request, 'new_model')
    # Now that we have our file, we will now try to load the model into
    # memory.
    # Now that we have our file, is it a zipfile?
    if not is_savezip_valid(file_path):
        raise cors_response(request, HTTPBadRequest('Incoming file is not a '
                                                    'valid zipfile!'))

    # Update the savefile if it is pre-SpillRefactor
    fp = update_savefile(file_path)
    resp_msg = 'OK'
    if (fp != file_path):
        resp_msg = 'UPDATED_MODEL'
    file_path = fp

    # now we try to load our model from the zipfile.
    session_lock = acquire_session_lock(request)
    log.info('  session lock acquired (sess:{}, thr_id: {})'
             .format(id(session_lock), current_thread().ident))
    try:
        log.info('loading our model from zip...')
        init_session_objects(request, force=True)
        refs = get_session_objects(request)

        new_model = Model.load(file_path, refs=refs)
        new_model._cache.enabled = False

        new_model._schema.register_refs(new_model._schema(), new_model, refs)
#         from ..views import implemented_types
#
#         RegisterObject(new_model, request, implemented_types)

        log.info('setting active model...')
        set_active_model(request, new_model.id)
    except Exception:
        raise cors_exception(request, HTTPBadRequest, with_stacktrace=True)
    finally:
        session_lock.release()
        log.info('  session lock released (sess:{}, thr_id: {})'
                 .format(id(session_lock), current_thread().ident))

    # We will want to clean up our tempfile when we are done.
    os.remove(file_path)

    return cors_response(request, Response(resp_msg))


@view_config(route_name='activate', request_method='OPTIONS')
@can_persist
def activate_model_options(request):
    return cors_response(request, request.response)


@view_config(route_name='activate', request_method='POST')
@can_persist
def activate_uploaded_model(request):
    '''
        Activates a new model from a zipfile that is stored in the
        uploads folder, and registers it as the current active model.
    '''
    clean_session_dir(request)

    zipfile_path, _name = activate_uploaded(request)
    log.info('Model zipfile: {}'.format(zipfile_path))

    # Now that we have our file, we will now try to load the model into
    # memory.
    # Now that we have our file, is it a zipfile?
    if not is_savezip_valid(zipfile_path):
        raise cors_response(request,
                            HTTPBadRequest('File is not a valid zipfile!'))

    # now we try to load our model from the zipfile.
    session_lock = acquire_session_lock(request)
    log.info('  session lock acquired (sess:{}, thr_id: {})'
             .format(id(session_lock), current_thread().ident))
    try:
        log.info('loading our model from zip...')
        init_session_objects(request, force=True)
        refs = get_session_objects(request)

        new_model = Model.load(zipfile_path, refs=refs)
        new_model._cache.enabled = False

        new_model._schema.register_refs(new_model._schema(), new_model, refs)
#         from ..views import implemented_types

#         RegisterObject(new_model, request, implemented_types)

        log.info('setting active model...')
        set_active_model(request, new_model.id)
    except Exception:
        raise cors_exception(request, HTTPBadRequest, with_stacktrace=True)
    finally:
        session_lock.release()
        log.info('  session lock released (sess:{}, thr_id: {})'
                 .format(id(session_lock), current_thread().ident))

    # We will want to clean up our temporary zipfile when we are done.
    os.remove(zipfile_path)

    return cors_response(request, Response('OK'))


@view_config(route_name='download')
def download_model(request):
    '''
        Here is where we save the active model as a zipfile and
        download it to the client
    '''
    my_model = get_active_model(request)

    if my_model:
        tf = tempfile.NamedTemporaryFile()
        filename = tf.name
        tf.close()

        json_, saveloc, refs = my_model.save(saveloc=filename)
        response_filename = ('{0}.gnome'.format(my_model.name))
        tf = open(saveloc, 'r+b')
        response = request.response
        response.content_type = 'application/zip'
        response.content_disposition = ('attachment; filename={0}'
                                        .format(response_filename))
        response.app_iter = FileIter(tf)
        return response
    else:
        raise cors_response(request, HTTPNotFound('No Active Model!'))


@view_config(route_name='persist', request_method='OPTIONS')
@can_persist
def save_and_persist_model_options(request):
    return cors_response(request, request.response)


@view_config(route_name='persist', request_method='POST')
@can_persist
def save_and_persist_model(request):
    '''
        Here is where we save the active model as a zipfile and
        store it in the persistent uploads area.
    '''
    my_model = get_active_model(request)

    if my_model:
        base_path = get_persistent_dir(request)

        requested_name = request.POST['name']
        if requested_name is not None:
            file_name = ('{0}.zip'.format(requested_name))
        else:
            file_name = ('{0}.zip'.format(my_model.name))

        my_model.save(saveloc=os.path.join(base_path, file_name))

        return cors_response(request, Response('OK'))
    else:
        raise cors_response(request, HTTPNotFound('No Active Model!'))


@persisted_files_api.get()
@can_persist
def get_uploaded_files(request):
    '''
        Returns a listing of the persistently uploaded files.

        If the web server is not configured to persist uploaded files,
        then we raise a HTTPNotImplemented exception

        TODO: We have an upload manager that has this functionality.  We need
              to prune this.
    '''
    return list_files(get_persistent_dir(request))
