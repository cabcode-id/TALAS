window.addEventListener("load", () => {
  var start = document.getElementById("start"),
    end = document.getElementById("end");

  start.onchange = () => {
    if (start.value == "") {
      end.min = "";
      end.value = "";
    } else {
      end.min = start.value;
      if (end.value != "" && new Date(end.value) < new Date(start.value)) {
        end.value = "";
      }
      
      if (end.value !== "") {
        window.location.href = `/news_page?start_date=${start.value}&end_date=${end.value}`;
      } else {
        end.showPicker();
      }
    }
  };
  
  end.onchange = () => {
    if (start.value !== "" && end.value !== "") {
      if (new Date(end.value) < new Date(start.value)) {
        alert("End date cannot be before start date.");
        end.value = start.value;
      } else {
        window.location.href = `/news_page?start_date=${start.value}&end_date=${end.value}`;
      }
    }
  };
});
