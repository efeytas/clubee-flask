let logged_student;
let logged_name;
let logged_number;
let logged_id;

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

/*function setGlobal(email){
  logged_student=email;
  console.log(logged_student);
  fetch('/getstudent/'+logged_student,{
    headers: {
      "auth-key":"0d5d254b22d390d9e11a132d53521a229da9fa0ae9ba009a76499f57c1d64e30",
    },
  })
    .then(response=> response.json())
    .then(data=> {
      data2=data[0]
      logged_id=data2[0];
      logged_name=data2[1];
      logged_student=data2[2];
      logged_number=data2[4];
    })
  getAdminsChapter()
}
let logged_user_chapter_id;

function getAdminsChapter(){
  fetch('/getchapterid/'+logged_id,{
    headers: {
      "auth-key":"0d5d254b22d390d9e11a132d53521a229da9fa0ae9ba009a76499f57c1d64e30",
    },
  })
    .then(response=> response.json())
    .then(data=> {
      data2=data[0]
      logged_user_chapter_id=data2[0];
    })
}*/

function viewEventsOfChapter(){
  //console.log(logged_id)
  //console.log(logged_name)
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
        outputHTML+=`<td> ${data[i][6]} </td>`;
        outputHTML+=`<td> ${data[i][3]} </td>`;
        outputHTML+=`<td> ${data[i][5]} </td>`;
        outputHTML+=`<td class="actions-cell">
          <div class="buttons right nowrap">
              <a href='/admin/chapter/editevent/?event_id=${data[i][0]}' class="button small blue">
                  <span class="icon"><i class="mdi mdi-pencil"></i></span>
              </a>
          </div>
        </td>`;
        outputHTML+='</tr>';
        //document.getElementById("event_id").innerHTML=data[i][5];
        //console.log(data[i][5]);
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
    const checkbox=document.getElementById("checkbox");
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
  fetch('/api/chapter/1',{
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

function viewEventData(){
  const urlParams = new URLSearchParams(window.location.search);
  const id = urlParams.get('event_id');
  console.log(id); 

  fetch('/api/events/'+id,{
    headers:{"auth-key":"0d5d254b22d390d9e11a132d53521a229da9fa0ae9ba009a76499f57c1d64e30",},
  })
  .then(response=> response.json())
  .then(data=> {

    data2=data[0]
    document.getElementById("event_id").innerHTML=data2[0];
    document.getElementById("event_name").innerHTML=data2[1];
    document.getElementById("event_date").innerHTML=data2[3];
    document.getElementById("event_description").innerHTML=data2[2];
    document.getElementById("event_status").innerHTML=data2[5];
    document.getElementById("event_highlight").innerHTML=data2[6];



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

