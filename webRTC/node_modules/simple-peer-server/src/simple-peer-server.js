class SimplePeerServer {
  constructor(httpServer, debug) {
    this.rooms = [];
    this.roomCounter = 0;

    this.studyRooms = {};

    this.debug = false;
    if (typeof debug !== 'undefined') {
      this.debug = true;
    }

    this.init(httpServer);
  }

  init(httpServer) {
    const ioServer = require('socket.io')(httpServer, {
     // path: "/?:id/socket.io",
     resource : "/1",
      cors: {
        origin: '*',
      },
    });
    let reg = new RegExp('^\/[0-9]+$')
    ioServer.of(reg).on('connection', (socket)=>{

       // logs server messages on the client
       socket.on('message', (message) =>
       this._handleMessage(message, socket),
     );
     socket.on('initiate peer', (room) =>
       this._handleInitiatePeer(room, socket),
     );
     socket.on('sending signal', (message) =>
       this._handleSendSignal(message, socket),
     );
     socket.on('create or join', () =>
       this._handleCreateOrJoin(socket, ioServer),
     );
     socket.on('hangup', () => this._handleHangup(socket));
     socket.on('disconnect', (reason) =>{ 
       this._handleDisconnect(reason) 
     } );
   });



/*
    ioServer.sockets.on('connection', (socket) => {

  
      // logs server messages on the client
      socket.on('message', (message) =>
        this._handleMessage(message, socket),
      );
      socket.on('initiate peer', (room) =>
        this._handleInitiatePeer(room, socket),
      );
      socket.on('sending signal', (message) =>
        this._handleSendSignal(message, socket),
      );
      socket.on('create or join', () =>
        this._handleCreateOrJoin(socket, ioServer),
      );
      socket.on('hangup', () => this._handleHangup(socket));
      socket.on('disconnect', (reason) =>{ 
        // custom code
       try{
        const room = socket.handshake['query']['private_path']
        const guest = socket.handshake['query']['guest']
        
        if (room in this.studyRooms){
          // remove guest 
          const idx = this.studyRooms[room].indexOf(guest)
          if (idx !==-1) this.studyRooms[room].splice(idx, 1)
          // check room is empty
          if (this.studyRooms[room].length===0) delete this.studyRooms[room]
          
        }
       }
       catch(err){
         console.log(err)
       }
        this._handleDisconnect(reason) 
      } );
    });
*/

  }

  _handleMessage(message, socket) {
    this.debug && console.log('Client said: ', message);
    // for a real app, would be room-only (not broadcast)
    socket.broadcast.emit('message', message);
  }

  _handleInitiatePeer(room, socket) {
    this.debug &&
      console.log('Server initiating peer in room ' + room);
    socket.to(room).emit('initiate peer', room);
  }
  _handleSendSignal(message, socket) {
    this.debug &&
      console.log('Handling send signal to room ' + message.room);
    socket.to(message.room).emit('sending signal', message);
  }

  _handleCreateOrJoin(socket, ioServer) {

    //get data
    const classroom = socket.handshake['query']['private_path']
    const guest = socket.handshake['query']['guest']
    const nsp = "/"+classroom
    //const clientIds = Array.from(ioServer.sockets.sockets.keys());
    const clientIds = Array.from(ioServer.of(nsp).sockets.keys());
    const numClients = clientIds.length;

    // custom code with evergreen
    this.debug && console.log('NUMCLIENTS, ' + numClients);


if (numClients === 1) {
  const room = this._createRoom(classroom);
  socket.join(room);
  socket.emit('created', room, socket.id);

  this.debug &&
    console.log(
      'Client ID ' + socket.id + ' created room ' + room,
    );
} else if (numClients === 2) {
  const room = this.rooms[this.rooms.length-1];
  ioServer.of(nsp).in(room).emit('join', room);
  socket.join(room);
  socket.emit('joined', room, socket.id);
  ioServer.of(nsp).in(room).emit('ready'); // not being used anywhere

  this.debug &&
    console.log(
      'Client ID ' + socket.id + ' joined room ' + room,
    );
} else if (numClients > 2) {
  for (let i = 0; i < numClients; i++) {
    if (socket.id !== clientIds[i]) {
      // create a room and join it
      const room = this._createRoom(classroom);
      socket.join(room);
      this.debug &&
        console.log(
          'Client ID ' + socket.id + ' created room ' + room,
        );
      socket.emit('created', room, socket.id);
      socket.emit('join', room);

      //
      this.debug &&
        console.log(
          'Client ID ' + clientIds[i] + ' joined room ' + room,
        );

      ioServer.of(nsp).sockets.get(clientIds[i]).join(room);
      ioServer.of(nsp).sockets
        .get(clientIds[i])
        .emit('joined', room, clientIds[i]);
    }
  }
}
    
  }

  _createRoom(classroom) {
    const room = 'room' + this.roomCounter +"_"+classroom;
    this.rooms.push(room);
    this.debug && console.log('number of rooms ' + this.rooms.length);
    this.roomCounter++;
    return room;
  }

  _handleHangup() {
    this.debug && console.log('received hangup');
  }

  _handleDisconnect(reason) {
    this.debug && console.log('disconnecting bc ' + reason);
    //custom code
  }
}

module.exports = SimplePeerServer;
