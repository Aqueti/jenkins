var session;

$(document).ready(function() {
    $(".caret").each(function(i, e) { $(e).on( "click", function() {
        $( this ).parent().children( ".nested" ).toggleClass( "active" );
        $( this ).toggleClass( "caret-down" );
        return;
    }); });

    $(".result").find("select").each(function(i,e) {
        $(e).trigger("change");
    });

    document.getElementById("username").innerText = session.username;
});

function set_vars(s) {
    session = s;
}

function gen_tree(tree, parent) {
  if (JSON.stringify(tree) === JSON.stringify({}) || typeof(tree["case_id"]) != "undefined") {
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

      li.appendChild(span);

      if (typeof(tree[key]["case_id"]) !== "undefined") {
        var s_div = document.createElement("div");
        s_div.className = "result";

        var select = document.createElement("select");

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

        s_div.appendChild(select);
        li.appendChild(s_div);
      }

      if (typeof(tree[key]["case_id"]) !== "undefined") {
        //span.innerText = tree[key].case_id + '. ' + span.innerText

        var ui_div = document.createElement("div");
        ui_div.className = "user-info";
        var ui_span = document.createElement("span");
        ui_span.innerText = "";

        if (typeof(tree[key]["timestamp"]) !== "undefined") {
          if (tree[key]["timestamp"] !== null) {
            ui_span.innerText = "last modified by " + tree[key]["user"] + " " + (new Date(tree[key]["timestamp"])).toLocaleString("en-US");
          }
        }

        ui_div.appendChild(ui_span);

        li.setAttribute("case_id", tree[key]["case_id"]);
        li.className = "case";

        li.appendChild(ui_div);
      }

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

    $(".result").find("select").each(function(i,e) {
        $(e).on("change", function(k) {
            var v = $(e).val();
            if (v == 1) {
                $(e).closest(".case").removeClass("fail");
                $(e).closest(".case").toggleClass("pass");
                $(e).closest(".case").find("div.github").remove();

                if (k.originalEvent) {
                    submit_json("/case_submit", {case_id: $(e).closest("li").attr("case_id"), result: $(e).find(":selected").val(), links: Array(), user: session.username, timestamp: Date.now()});
                }
            } else if (v == 0) {
                $(e).closest(".case").removeClass("pass");
                $(e).closest(".case").toggleClass("fail");

                if ($(e).closest(".case").find(".github").length == 0) {
                    $(e).closest(".case").append("<div class='github'><ul><li class='add-link'>add github link</li></ul></div>");
                }

                $(e).closest(".case").find("li.add-link").on("click", function() {
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

                                //if (k.originalEvent) {
                                submit_json("/case_submit", {case_id: $(e).closest("li").attr("case_id"), result: $(e).find(":selected").val(), links: linksArr, user: session.username, timestamp: Date.now()});
                                //}
                            }
                        });
                    }
                });

                if (k.originalEvent) {
                    submit_json("/case_submit", {case_id: $(e).closest("li").attr("case_id"), result: $(e).find(":selected").val(), links: Array(), user: session.username, timestamp: Date.now()});
                }
            } else {
                $(e).closest(".case").removeClass("pass");
                $(e).closest(".case").removeClass("fail");
                $(e).closest(".case").find("div.github").remove();

                if (k.originalEvent) {
                    submit_json("/case_submit", {case_id: $(e).closest("li").attr("case_id"), result: $(e).find(":selected").val(), links: Array(), user: session.username, timestamp: Date.now()});
                }
            }

            if (k.originalEvent) {
                $(e).parent().find("div.user-info").find("span").text("last modified by " + session.username + " " + (new Date()).toLocaleString("en-US"));
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
