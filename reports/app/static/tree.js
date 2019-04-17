$(document).ready(function() {
    $(".caret").each(function(i, e) { $(e).on( "click", function() {
        $( this ).parent().children( ".nested" ).toggleClass( "active" );
        $( this ).toggleClass( "caret-down" );
        return;
    }); });
});

function gen_tree(tree, parent) {
  if (JSON.stringify(tree) === JSON.stringify({})) {
    return;
  }

  for (var key in tree) {
      var ul = document.createElement("ul");

      var li = document.createElement("li");
      var span = document.createElement("span");
      span.innerText = key;

      if (parent.tagName.toLowerCase() != 'div') {
        ul.setAttribute("class", "nested active");
        parent.getElementsByTagName('span')[0].setAttribute("class", "caret caret-down");
      }

      if (JSON.stringify(tree[key]) === JSON.stringify({})) {
        var select = document.createElement("select");
        select.className = "result";

        var results = [[-1,"N/A"],[0,"FAIL"],[1,"PASS"]];

        for (var i = 0; i < results.length; i++) {
            var option = document.createElement("option");
            option.value = results[i][0];
            option.text = results[i][1];
            select.appendChild(option);
        }

        li.className = "req";
        li.append(select);
      }

      li.appendChild(span);

      var parent_ul = parent.querySelector('ul')
      if (parent_ul === null) {
        ul.appendChild(li);
        parent.appendChild(ul);
      }
      else {
        parent_ul.appendChild(li);
      }

      gen_tree(tree[key], li);
  }
}

function add_listeners() {
    dds = Array(document.getElementById("proj"), document.getElementById("branch"), document.getElementById("build"));
    for (var i = 0; i < dds.length; i++) {
      dds[i].addEventListener("change", function() {
        document.getElementById('pbb').querySelector('#submit').click();
      });
    }

    elems = document.getElementsByClassName('result');
    for (var i = 0; i < elems.length; i++) {
      elems[i].addEventListener("change", function() {
        e = this;
        while (!e.classList.contains("req")) {
            e = e.parentElement;
        }

        e.classList.remove("pass", "fail");

        var v = this.selectedOptions[0].value;
        if (v == 1) {
            e.classList.toggle('pass');
        } else if (v == 0) {
            e.classList.toggle('fail');
        } else {

        }
      });
    }
}

function restoreState(state) {
    //$('#proj').prop('selected', true)
    for (var key in state) {
        document.getElementById(key).value = state[key];
    }
}


function submit(data) {
	$.ajax({
        type: "POST",
        url: this,
        contentType: "text/plain",
        data: JSON.stringify(data),

        crossDomain: true,
    });
}

function update() {
  $.get("", function(data) {
    $("#div").html(data);
    window.setTimeout(update, 5000);
  });
}