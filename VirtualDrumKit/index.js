var numberOfDrumButton=document.querySelectorAll(".drum").length;

for(var i=0;i<numberOfDrumButton;i++){
    document.querySelectorAll(".drum")[i].addEventListener("click",Clicked);
    function Clicked(){
        var audio= new Audio('./sounds/tom-1.mp3');
        audio.play();
    }

}

for(var i=0;i<numberOfDrumButton;i++){
    document.querySelectorAll(".drum")[i].addEventListener("keydown",Clicked);
    function Clicked(){
        var audio= new Audio('./sounds/tom-3.mp3');
        audio.play();
    }

}