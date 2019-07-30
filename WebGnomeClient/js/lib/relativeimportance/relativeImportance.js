define(function(){
  var Triangle = (function(selector, opts){
        this.canvasHTML = document.getElementById(selector);
        this.ctx = this.canvasHTML.getContext('2d');
        var rect = this.canvasHTML.getBoundingClientRect();
        this.offset = {top: rect.top + document.body.scrollTop, left: rect.left + document.body.scrollLeft};
        var boxSize = this.canvasHTML.width;
        this.pressed = false;
        
        var _Opts = {
            sideLength: 100,
            point1: {label: 'Point 1', color: '#EDC240'},
            point2: {label: 'Point 2', color: '#CB4B4B'},
            point3: {label: 'Point 3', color: '#AFD8F8'},
            callback: null
        };
        
        var optsKeys = Object.keys(opts);
        
        for (var i = 0; i < optsKeys.length; i++){
            if (typeof opts[optsKeys[i]] !== 'object'){
                _Opts[optsKeys[i]] = opts[optsKeys[i]];
            } else if (opts[optsKeys[i]] !== null){
                for (var key in opts[optsKeys[i]]){
                    if (opts[optsKeys[i]][key] !== undefined){
                        _Opts[optsKeys[i]][key] = opts[optsKeys[i]][key];
                    }
                }
            }
        }
          
        this.sideLength = _Opts.sideLength;
        this.callback = _Opts.callback;
        
        var triHeight = this.sideLength * (Math.sqrt(3) / 2);
        this.vertTrans = ((boxSize - triHeight) / 2);// - this.offset.top;
        var horizTrans = ((boxSize - this.sideLength) / 2);// - this.offset.left;
          
        var point1 = {x: boxSize / 2, y: this.vertTrans, label: _Opts.point1.label, color: _Opts.point1.color};
        var point2 = {x: horizTrans, y: this.vertTrans + triHeight, label: _Opts.point2.label, color: _Opts.point2.color};
        var point3 = {x: horizTrans + this.sideLength, y: this.vertTrans + triHeight, label: _Opts.point3.label, color: _Opts.point3.color};
      
        this.points = [point1, point2, point3];

        this.path = this.getPath();
    });
    
    Triangle.prototype.textMidPoint = function(text){
        return this.ctx.measureText(text).width / 2;
    };

    Triangle.prototype.addListeners = function(){
        this.canvasHTML.addEventListener('mouseup', function(){
            this.pressed = false;
        }.bind(this));
    
        this.canvasHTML.addEventListener('mousedown', function(){
            this.pressed = true;
        }.bind(this));

        this.canvasHTML.addEventListener('mousedown', function(ev){
            Triangle.prototype.draw.call(this, ev);
        }.bind(this));

        this.canvasHTML.addEventListener('mousemove', function(ev) {
            if (!this.pressed){
                return;
            }
            Triangle.prototype.draw.call(this, ev);
        }.bind(this));
    };
    
    Triangle.prototype.draw = function(ev){
        var mouseClick = Triangle.prototype.getMousePosition.call(this, ev);
        var collision = this.ctx.isPointInPath(this.path, mouseClick.x, mouseClick.y);
        if (ev === undefined || collision){
            this.ctx.clearRect(0, 0, this.canvasHTML.width, this.canvasHTML.height);
            Triangle.prototype.applyPointGradients.call(this, ev);
            this.ctx.stroke(this.path);
            this.ctx.fillStyle = 'black';
            this.drawText();
            this.drawCircle(ev);
         }
        Triangle.prototype.relativeDistances.call(this, ev);
        if (ev === undefined){
          Triangle.prototype.addListeners.call(this);
        }
    };
    
    Triangle.prototype.applyPointGradients = function(ev){
        var radius = this.sideLength * (Math.sqrt(3) / 3);
        for (var i = 0; i < this.points.length; i++){
            var point = this.points[i];
            var gradient = this.ctx.createRadialGradient(point.x, point.y, 2 * radius, point.x, point.y, 0);
            gradient.addColorStop(0, 'rgba(255,255,255,0)');
            gradient.addColorStop(0.75, point.color);
            gradient.addColorStop(1, point.color);
            this.ctx.fillStyle = gradient;
            this.ctx.save();
            this.ctx.beginPath();
            this.ctx.arc(point.x, point.y, 2 * radius, 0, 2 * Math.PI);
            this.ctx.clip(this.path);
            this.ctx.closePath();
            this.ctx.fill();
            this.ctx.restore();
        }
    };

    Triangle.prototype.getMousePosition = function(ev){
        if (ev === undefined){
              return {x: 0, y: 0};
          }
          var coords;
          if (ev['layerX'] !== undefined) {
              coords = {
                  x: ev.layerX,
                  y: ev.layerY
              };
          } else {
              coords = {
                x: ev.x,
                y: ev.y
              };
          }
          return coords;
    };
    
    Triangle.prototype.drawCircle = function(ev){
        var coords;
        var initialY = this.vertTrans + this.sideLength * (Math.sqrt(3) / 3);
        if (ev === undefined){
              coords = {x: this.canvasHTML.width / 2, y: initialY};
        } else {
            coords = Triangle.prototype.getMousePosition.call(this, ev);
        }
        this.ctx.beginPath();
        this.ctx.arc(coords.x, coords.y, 5, 0, Math.PI * 2, true);
        this.ctx.closePath();
        this.ctx.fill();
        this.coords = coords;
    };
    
    Triangle.prototype.drawText = function(){
        var scalingFact = 1 / 10;
        var fontSize = (scalingFact * this.sideLength);
        this.ctx.font = fontSize + "px arial";
        this.ctx.fillText(this.points[0].label, this.points[0].x - this.textMidPoint(this.points[0].label), this.points[0].y - fontSize / 2);
        for (var i = 1; i < this.points.length; i++){
            this.ctx.fillText(this.points[i].label, this.points[i].x - this.textMidPoint(this.points[i].label), this.points[i].y + fontSize);
        }
    };
    
    Triangle.prototype.getPath = function(){
        var path = new Path2D();
        path.moveTo(this.points[0].x, this.points[0].y);
        for (var i = this.points.length - 1; i > 0; i--){
            path.lineTo(this.points[i].x, this.points[i].y);
        }
        path.lineTo(this.points[0].x, this.points[0].y);
        return path;
    };
    
    Triangle.prototype.percentDistances = function(){
        var percents = {};
        for (var key in this.distances){
            percents[key] = {data: this.getPercent(this.distances[key].data), color: this.distances[key].color};
        }
        
        if (this.callback !== null){
          this.callback(percents);
        }
    };
    
    Triangle.prototype.getPercent = function(distance){
        return (1 - (2 * distance / (this.distancesSum))) * 100;
    };
    
    Triangle.prototype.relativeDistances = function(ev){
        var distances = {};
        var sum = 0;
        for (var i = 0; i < this.points.length; i++){
            var distance = this.distanceTo(this.points[i]);
            distances[this.points[i].label] = {data: distance, color: this.points[i].color};
            sum += distance;
        }
        this.distancesSum = sum;
        this.distances = distances;
        this.percentDistances();
    };
    
    Triangle.prototype.distanceTo = function(point){
        return Math.sqrt(Math.pow(point.x - this.coords.x, 2) + Math.pow(point.y - this.coords.y, 2));
    };

    return Triangle;
});