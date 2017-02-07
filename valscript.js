
function updatediv(content){
    document.getElementById("resultcontent").innerHTML = content;
}

function initform(){

    $("#idform").submit(function(e) {
             window.setInterval(function(){ refreshvotes(); }, 10000);
            document.getElementById('formdiv').style.display='none'; // hide voting div
            var url = "votedajax"; // the script where you handle the form input.
            var test=$(this).serialize();
            $.ajax({
                   type: "POST",
                   url: url,
                   data: $("#idform").serialize(), // serializes the form's elements.
                   success: function(data)
                   {
                       //alert(data); // show response from the php script.
                       updatediv(data);
                   }
                 });

            e.preventDefault(); // avoid to execute the actual submit of the form.
        });
}


function refreshvotes(){

            $.ajax({
                   type: "POST",
                   url: "refresh",
                   data: "", // serializes the form's elements.
                   success: function(data)
                   {
                       //alert(data); // show response from the php script.
                       updatediv(data);
                   }
                 });
}
