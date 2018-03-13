var CANVAS_WIDTH = 352;
var CANVAS_HEIGHT = 352;

var ROOM_WIDTH = 11;
var ROOM_HEIGHT = 11;

var TILE_SIZE = 16;
var TILE_SCALE = 2;

var canvas = document.getElementById("room");
var context = canvas.getContext("2d");
var spritesheet = new Image();
spritesheet.src = "images/things.png";

var doors = {
    north: {x: Math.floor(ROOM_WIDTH/2), y:0},
    south: {x: Math.floor(ROOM_WIDTH/2), y:ROOM_HEIGHT-1},
    west: {x: 0, y:Math.floor(ROOM_HEIGHT/2)},
    east: {x: ROOM_WIDTH-1, y:Math.floor(ROOM_HEIGHT/2)}
};

var characterImages = {
    'Power Kjell': {x: 1, y:17},
    'Max Overflow': {x: 0, y:18},
}

function _move(exit) {
    request = new XMLHttpRequest();
    request.onreadystatechange = () => {
        if (request.readyState === 4) {
            if (request.status === 200) {

                return draw(JSON.parse(request.responseText));
            }
            console.log('error!');
        }
    };
    request.open('POST', '/mud/lime-mud/move/');
    request.setRequestHeader('Content-Type', 'application/json');
    console.log("sending move", {exit})
    request.send(JSON.stringify({exit}))
}

document.onkeydown = function(event) {
    event = event || window.event;

    keys = {
        37: 'west',
        39: 'east',
        38: 'north',
        40: 'south',
    }
    if (keys[event.keyCode]) {
        return _move(keys[event.keyCode]);
    }
    console.log('unhandled key');
};

function draw(data){
    console.log(data);
    document.getElementById("content").innerHTML = data.name; 
    context.fillStyle = "#000";
    context.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
    for (var y=0; y<ROOM_HEIGHT;y++) {
        for (var x=0; x<ROOM_WIDTH;x++) {

            drawFloor(context, x, y);

            if (x == 0 || x == ROOM_WIDTH-1 || y == 0 || y == ROOM_HEIGHT-1) {
                drawWall(context, x, y);
            }

            data.exits.map((exit) => {
                if (doors[exit].x == x && doors[exit].y == y) {
                    drawDoor(context, x, y);
                }
            });

            if (x == Math.floor(ROOM_WIDTH/2) && y == Math.floor(ROOM_HEIGHT/2)) {
                drawCharacter(context, x, y, data.characters[0]);
            }

            if (x == Math.floor(ROOM_WIDTH/2) + 1 && y == Math.floor(ROOM_HEIGHT/2)) {
                if (data.characters.length == 2) {
                    drawCharacter(context, x, y, data.characters[1]);
                }
            }


            if (x == Math.floor(ROOM_WIDTH/2) && y == Math.floor(ROOM_HEIGHT/4)) {
                console.log('key time');
                if (data.items.indexOf("Rusty Key") != -1) {
                    console.log('key time 2');
                    drawKey(context, x, y);
                }
            }
        }
    }
}

function drawTile(context, x, y, tilex, tiley) {
    context.drawImage(
        spritesheet,
        tilex*TILE_SIZE,
        tiley*TILE_SIZE,
        TILE_SIZE,
        TILE_SIZE,
        x*TILE_SIZE*TILE_SCALE,
        y*TILE_SIZE*TILE_SCALE,
        TILE_SIZE*TILE_SCALE,
        TILE_SIZE*TILE_SCALE
    );
}

function drawWall(context, x, y) {
    var tilex = 0;
    var tiley = 21;
    drawTile(context, x, y, tilex, tiley);
}

function drawFloor(context, x, y) {
    var tilex = 7;
    var tiley = 23;
    drawTile(context, x, y, tilex, tiley);
}

function drawDoor(context, x, y) {
    var tilex = 0;
    var tiley = 0;
    drawTile(context, x, y, tilex, tiley);
}

function drawCharacter(context, x, y, name) {
    var tilex = characterImages[name].x;
    var tiley = characterImages[name].y;
    drawTile(context, x, y, tilex, tiley);
}

function drawKey(context, x, y) {
    var tilex = 0;
    var tiley = 25;
    drawTile(context, x, y, tilex, tiley);
}

function getData(onSuccess) {
    const request = new XMLHttpRequest();

    request.onreadystatechange = () => {
        if (request.readyState === 4) {
            if (request.status === 200) {

                return onSuccess(JSON.parse(request.responseText));
            }
            console.log('error!');
        }
    };
    request.open('GET', '/mud/lime-mud/look/', true);
    request.send(null);
}

spritesheet.onload = function(event) {
    getData(draw);
}
