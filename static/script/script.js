function viewEvents(){
    fetch('/api/events/2',{
      headers: {
        "auth-key":"0d5d254b22d390d9e11a132d53521a229da9fa0ae9ba009a76499f57c1d64e30",
      },
    })
      .then(response=> response.json())
      .then(data=> {

        data2=data[0];
        document.getElementById("array").innerHTML=data2;
        document.getElementById("event-name").innerHTML=data2[1];
        document.getElementById("description").innerHTML=data2[2];
        document.getElementById("highlighted").innerHTML=data2[6];
        document.getElementById("event-date").innerHTML=data2[3];
        document.getElementById("event-status").innerHTML=data2[5];
      })

}

function viewAllEvents(){
    fetch('/api/events/all',{
      headers: {
        "auth-key":"0d5d254b22d390d9e11a132d53521a229da9fa0ae9ba009a76499f57c1d64e30",
      },
    })
      .then(response=> response.json())
      .then(data=> {

        var outputHTML="";
        data2=data[0]
        for(var i=0;i<data.length;i++){
          outputHTML+='<tr>';
          outputHTML+=`<td> ${data[i][1]} </td>`;
          outputHTML+=`<td> ${data[i][2]} </td>`;
          outputHTML+=`<td> ${data[i][6]} </td>`;
          outputHTML+=`<td> ${data[i][3]} </td>`;
          outputHTML+=`<td> ${data[i][5]} </td>`;
          outputHTML+='</tr>';
        }
        document.getElementById("output_tr").innerHTML=outputHTML;
      })

}


function viewActiveMembers(){
    fetch('/api/activechapters/1',{
      headers: {
        "auth-key":"0d5d254b22d390d9e11a132d53521a229da9fa0ae9ba009a76499f57c1d64e30",
      },
    })
      .then(response=> response.json())
      .then(data=> {

        data2=data[0]
        document.getElementById("studen-name").innerHTML=data2[1];
        document.getElementById("student-id").innerHTML=data2[2];
      })
}

function addEventsJs(){
  const form=document.getElementById('myForm');

  form.addEventListener('submit', (event)=>{
      //event.preventDefault();
      const formData=new FormData(form);
      const event_name=formData.get("name");
      const event_description=formData.get("description");
      const event_date=formData.get("event_date");
      const event_photolink=formData.get("photolink");
      const event_status=formData.get("eventstatus");
      const event_highlighted=formData.get("highlighted");
      const event_chapter_id=formData.get("chapter_id");
      fetch('/api/createevent',{
        method: 'POST',
        headers: {
          //"Server" : "Werkzeug/2.2.2 Python/3.8.10",
          //"Content-Length": data.length,
          //"Content-Type": "application/json",
          "auth-key":"0d5d254b22d390d9e11a132d53521a229da9fa0ae9ba009a76499f57c1d64e30",
        },
        body: JSON({name: event_name},{description: event_description},{event_date: event_date},{photolink: event_photolink},
          {eventstatus: event_status},{highlighted: event_highlighted}, {chapter_id: event_chapter_id}
        )
  })

});
}