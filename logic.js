async function output()
{
    document.getElementById("output").innerText = "";
    JOB = document.getElementById("url").value;
    RESUME = document.getElementById("resume").files[0];
    const formData = new FormData();

    formData.append('job_url',JOB);
    formData.append('resume',RESUME);
    const x = document.getElementsByClassName('loader')[0];
    x.style.zIndex = 9999;
    x.style.opacity = 1;

    const y = document.querySelector('#url');
    y.disabled = true;

    const z = document.querySelector('#resume');
    z.disabled = true;



    x.innerText = 'Generating Email...';
    const response = await fetch('https://backendemail-vl1a.onrender.com/generate-email',{method : "POST" , body : formData} );
    if (!response.ok) {
    const err = await response.json();
    console.log(err);
    return;
  }
  const data = await response.json();
  console.log("Email received:", data.email);
  document.getElementById("output").innerText = data.email;

  x.style.opacity = 0;
  x.style.zIndex = 0;
  y.disabled = false;
  z.disabled = false;
  
  console.log("Full response:", JSON.stringify(data));
}