window.addEventListener( "load", function () {
  function sendData(data) {
    const XHR = new XMLHttpRequest();

    const FD = new FormData(form);

    for(i in data) {
      FD.append(i,data[name]);
    }

    XHR.addEventListener( "load", function(event) {
      alert( event.target.responseText );
    } );

    XHR.addEventListener( "error", function( event ) {
      alert( 'Oops! Something went wrong.' );
    } );

    XHR.open( "POST", "./database_functions.py" );

    XHR.send(FD);
  }
  let form = document.getElementById( "form" );

    form.addEventListener( "submit", function ( event ) {
    event.preventDefault();

    sendData();
  } );
} );
