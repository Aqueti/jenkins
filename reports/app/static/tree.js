$(document).ready(function() {
    $(".caret").each(function(i, e) { $(e).on( "click", function() {
        $( this ).parent().children( ".nested" ).toggleClass( "active" );
        $( this ).toggleClass( "caret-down" );
        return;
    }); });

    $(".result").each(function(i,e) {
        $(e).trigger("change");
    });
});

function gen_tree(tree, parent) {
  if (JSON.stringify(tree) === JSON.stringify({}) || typeof(tree["req_id"]) != "undefined") {
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

      if (typeof(tree[key]["req_id"]) !== "undefined") {
        var select = document.createElement("select");
        select.className = "result";

        var results = [[-1,"N/A"],[0,"FAIL"],[1,"PASS"]];
        for (var i = 0; i < results.length; i++) {
            var option = document.createElement("option");
            option.value = results[i][0];
            option.text = results[i][1];
            select.appendChild(option);

            if (results[i][0] == tree[key]["result"]) {
                option.setAttribute("selected", "selected");
            }
        }

        li.setAttribute("req_id", tree[key]["req_id"]);
        li.className = "req";
        li.appendChild(select);
      }

      li.appendChild(span);

      if (typeof(tree[key]["links"]) !== "undefined") {
        if (tree[key]["links"]) {
        var links_div = document.createElement("div");
        links_div.className = "github";

        var links_ul = document.createElement("ul");
        var links_li = document.createElement("li");
        links_li.className = "add-link";
        links_li.innerText = "add github link";
        links_ul.appendChild(links_li);

        for (var i = 0; i < tree[key]["links"].length; i++) {
            var links_li2 = document.createElement("li");
            var links_a = document.createElement("a");
            links_a.href = tree[key]["links"][i];
            links_a.innerText = tree[key]["links"][i];

            links_li2.appendChild(links_a);
            links_ul.appendChild(links_li2);
        }

        links_div.appendChild(links_ul);
        li.appendChild(links_div);
        }
      }

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

function submit_json(url, data) {
	$.ajax({
	    url: url,
        type: "POST",
        data: JSON.stringify(data),
        dataType: "json",
        contentType: "application/json;charset=utf-8"
    });
}

function update() {
  $.get("", function(data) {
    $("#id").html(data);
    window.setTimeout(update, 5000);
  });
}

function add_listeners() {
    dds = Array(document.getElementById("proj"), document.getElementById("branch"), document.getElementById("build"));
    for (var i = 0; i < dds.length; i++) {
      dds[i].addEventListener("change", function() {
        document.getElementById('pbb_submit').click();
      });
    }

    $(".result").each(function(i,e) {
        $(e).on("change", function() {
            var v = $(e).val();
            if (v == 1) {
                $(e).closest(".req").removeClass("fail");
                $(e).closest(".req").toggleClass("pass");
                $(e).closest(".req").find("div.github").remove();

                submit_json("/req_submit", {req_id: $(e).parent().attr("req_id"), result: $(e).find(":selected").val(), links: Array()});
            } else if (v == 0) {
                $(e).closest(".req").removeClass("pass");
                $(e).closest(".req").toggleClass("fail");

                if ($(e).closest(".req").find(".github").length == 0) {
                    $(e).closest(".req").append("<div class='github'><ul><li class='add-link'>add github link</li></ul></div>");
                }

                $(e).closest(".req").find("li.add-link").on("click", function() {
                    var div = $(this).closest("div.github");
                    if (div.find(".gt-text").length == 0) {
                        div.append("<input type='text' class='gt-text' placeholder='put a link here'/>");
                        div.find(".gt-text").focus();
                        div.find(".gt-text").on("focusout", function() {
                            var val = $(this).val();
                            $(this).remove();
                            if (val != "") {
                                div.find("ul").append("<li><a href='" + val + "'>" + val + "</a></li>");

                                var linksArr = Array();
                                div.find("a").each(function(i,e) {
                                    linksArr.push($(this).attr("href"));
                                });

                                submit_json("/req_submit", {req_id: $(e).parent().attr("req_id"), result: $(e).find(":selected").val(), links: linksArr});
                            }
                        });
                    }
                });

                submit_json("/req_submit", {req_id: $(e).parent().attr("req_id"), result: $(e).find(":selected").val()});
            } else {
                $(e).closest(".req").removeClass("pass");
                $(e).closest(".req").removeClass("fail");
                $(e).closest(".req").find("div.github").remove();

                submit_json("/req_submit", {req_id: $(e).parent().attr("req_id"), result: $(e).find(":selected").val(), links: Array()});
            }
        });
    });
}

function restoreState(state) {
    //$('#proj').prop('selected', true)
    for (var id in state) {
        document.getElementById(id).value = state[id][0];
    }
}
