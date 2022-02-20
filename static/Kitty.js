function random_kitty(){
    fetch("https://api.thecatapi.com/v1/images/search").then(response => {
        response.json().then(data => {
          console.log(data[0].url);
          document.querySelector("#Cat-Image").src = data[0].url;
          document.querySelector("#download_pic").href = data[0].url;
        });
    });
    
}

