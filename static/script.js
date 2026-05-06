async function analyzeError(){
    const errorinput= document.getElementById("errorInput");
    const loading=document.getElementById("loading");
    const resultBox=document.getElementById("resultBox");

    const summary=document.getElementById("summary");
    const rootCause=document.getElementById("rootCause");
    const fixSteps=document.getElementById("fixSteps");

    const errorText=errorinput.ariaValueMax.trim();

    if(errorText === ""){
        alert("Please paste an error log first");
        return;
    }

    loading.classList.remove("hidden");
    resultBox.classList.add("hidden");

    try{
        const response= await fetch("/analyze", {
            method: "POST",
            header:{
                "Content-Type":"application/json"
            },
            body: JSON.stringify({
                error_text: errorText
            })
            });

            const data=await response.json();
            
            if(!data.success){
                alert(data.message || "Something went wrong.");
                return;
            }

            summary.textContent=data.analysis.summary;
            rootCause.textContent=data.analysis.root_cause;

            fixSteps.innerHTML="";

            data.analysis.fix_steps.forEach(function(step){
                const li= document.createElement("li");
                li.textContent= step;
                fixSteps.appendChild(li);
            });
            resultBox.classList.remove("hidden");
        }
        catch(error){
            alert("Failed to connect to backend.");
            console.error(error);
        }finally{
            loading.classList.add("hidden");
        }
}
