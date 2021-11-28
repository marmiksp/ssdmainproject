
console.log(note)

var step1 = document.querySelector('#step1')
var step2 = document.querySelector('#step2')
var step3 = document.querySelector('#step3')
var step4= document.querySelector('#step4')
var step5= document.querySelector('#step5')

var colorarray=Array("orchid","dodgerblue","darkturquoise","tomato","deeppink","yellow")







for (var i = 0; i < note.length; i++) {
    if(note[i].step==1)
    {
     
      var ele = document.createElement('div')
   ele.classList.add('note')
   ele.style.backgroundColor=colorarray[colorarray.length * Math.random() | 0]
   ele.innerHTML = note[i].content
   step1.appendChild(ele)
    }

    else if(note[i].step==2)
    {
        var ele = document.createElement('div')
        ele.classList.add('note')
        ele.style.backgroundColor=colorarray[colorarray.length * Math.random() | 0]
       ele.innerHTML = note[i].content
        step2.appendChild(ele)
        console.log(note[i].step)
    }
    else if(note[i].step==3)
    {
        var ele = document.createElement('div')
        ele.classList.add('note')
        ele.style.backgroundColor=colorarray[colorarray.length * Math.random() | 0]
        
        ele.innerHTML = note[i].content
        step3.appendChild(ele)
        console.log(note[i].step)
    }
    else if(note[i].step==5)
    {
        var ele = document.createElement('div')
        ele.classList.add('note')
        ele.style.backgroundColor=colorarray[colorarray.length * Math.random() | 0]
       
        ele.innerHTML = note[i].content
        step5.appendChild(ele)
        console.log(note[i].step)
    }
    else
    {
       
    }

}