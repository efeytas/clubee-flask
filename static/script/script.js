function viewEvents(){
    fetch('/api/events/1',{
      headers: {
        "auth-key":"0d5d254b22d390d9e11a132d53521a229da9fa0ae9ba009a76499f57c1d64e30",
      },
    })
      .then(response=> response.json())
      .then(data=> {

        data2=data[0];
        var outputHTML="";
        for(var i=0;i<data.length;i++){
          outputHTML+='<tr>';
          outputHTML+=`<td> ${data[i][1]} </td>`;
          outputHTML+=`<td> ${data[i][2]} </td>`;
          outputHTML+=`<td> ${data[i][6]} </td>`;
          outputHTML+=`<td> ${data[i][3]} </td>`;
          outputHTML+=`<td> ${data[i][5]} </td>`;
          outputHTML+=`<td class="actions-cell">
          <div class="buttons right nowrap">
              <a href="edit_member.html" class="button small blue">
                  <span class="icon"><i class="mdi mdi-pencil"></i></span>
              </a>
          </div>
        </td>`;
          outputHTML+='</tr>';
        }
        document.getElementById("output_tr").innerHTML=outputHTML;
      })

}


function viewEventsOfChapter(){
  fetch('/admin/events/1',{
    headers: {
      "auth-key":"0d5d254b22d390d9e11a132d53521a229da9fa0ae9ba009a76499f57c1d64e30",
    },
  })
    .then(response=> response.json())
    .then(data=> {

      data2=data[0];
      var outputHTML="";
      for(var i=0;i<data.length;i++){
        outputHTML+='<tr>';
        outputHTML+=`<td> ${data[i][1]} </td>`;
        outputHTML+=`<td> ${data[i][2]} </td>`;
        outputHTML+=`<td> ${data[i][6]} <input type="checkbox" id="checkbox" onclick="sendData()"></td>`;
        outputHTML+=`<td> ${data[i][3]} </td>`;
        outputHTML+=`<td> ${data[i][5]} </td>`;
        outputHTML+=`<td class="actions-cell">
          <div class="buttons right nowrap">
              <a href='/admin/chapter/editevent' class="button small blue">
                  <span class="icon"><i class="mdi mdi-pencil"></i></span>
              </a>
          </div>
        </td>`;
        outputHTML+='</tr>';
      }
      document.getElementById("output_tr").innerHTML=outputHTML;
    })

}


function sendData(){
  var checkbox =document.getElementById("checkbox");
  var data={"value":checkbox.checked};
  fetch("/api/highlight-event", {
    method: "POST",
    body: JSON.stringify(data),
    headers: {
      "Content-Type": "application/json",
      "auth-key":"0d5d254b22d390d9e11a132d53521a229da9fa0ae9ba009a76499f57c1d64e30",
    }
  })
  .then(response => response.json())
  .then(data => {
    console.log(data);
  });
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

function viewChapterProfile(){
  fetch('/api/chapter/4',{
    headers:{"auth-key":"0d5d254b22d390d9e11a132d53521a229da9fa0ae9ba009a76499f57c1d64e30",},
  })
  .then(response=> response.json())
  .then(data=> {

    data2=data[0]
    document.getElementById("chapter_id").innerHTML=data2[0];
    document.getElementById("data1").innerHTML=data2[1];
    document.getElementById("data2").innerHTML=data2[2];


  })
}


function viewActiveMembers(){
    fetch('/admin/activemembersinchapter/1',{
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
          outputHTML+=`<td> ${data[i][4]} </td>`;
          outputHTML+=`<td> ${data[i][2]} </td>`;
          outputHTML+='</tr>';
        }
        document.getElementById("active_members").innerHTML=outputHTML;
      })
}

function viewAdminOfChapter(){
  fetch('/admin/adminofchapter/1',{
    headers: {
      "auth-key":"0d5d254b22d390d9e11a132d53521a229da9fa0ae9ba009a76499f57c1d64e30",
    },
  })
    .then(response=> response.json())
    .then(data=> {
      data2=data[0]

      document.getElementById("name").innerHTML=data2[1];
      document.getElementById("e-mail").innerHTML=data2[2];
      document.getElementById("studentnumber").innerHTML=data2[4];



    })
}

/*
  const form=document.getElementById('myForm');
  if(form){
  console.log("Screen opened")
  form.addEventListener('submit', function(){
      
      console.log("Event listened")
//      const formData=new FormData(form);
      const event_name=getElementById("name").value
      const event_description=getElementById("description").value
      const event_date=getElementById("event_date").value
      const event_photolink=getElementById("photolink").value
      const event_status=getElementById("eventstatus").value
      const event_highlighted=getElementById("highlighted").value
      const event_chapter_id=getElementById("chapter_id").value
      fetch('/api/createevent',{
        method: 'POST',
        headers: {
          //"Server" : "Werkzeug/2.2.2 Python/3.8.10",
          //"Content-Length": data.length,
          //"Content-Type": "application/json",
          "auth-key":"0d5d254b22d390d9e11a132d53521a229da9fa0ae9ba009a76499f57c1d64e30",
        },
        body: JSON({
          name: event_name,
          description: event_description,
          event_date: event_date,
          photolink: event_photolink,
          eventstatus: event_status,
          highlighted: event_highlighted,
           chapter_id: event_chapter_id}),
  })
        .then(response=>response.json())
        .then(data=>console.log(data)
        )
        .catch((error) => {
          console.error('There has been a problem with your fetch operation:', error);
        });

});
  }
*/