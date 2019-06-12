$(document).ready(function() {
   var href = $(location).attr('href');
   var pages = ["Version", "Status", "History"];

   for (var i = 0; i < pages.length; i++) {
     if (href.includes(pages[i].toLowerCase())) {
        $(".navbar-nav").find("a:contains('" + pages[i] + "')").closest("li").addClass("active");
        break;
     }
   }

   if ($(".navbar-nav").find("li.active").length == 0) {
     $(".navbar-nav").find("a:contains('Version')").closest("li").addClass("active");
   }
});


function gen_info(info, elem) {
    system_arr = [...new Set(info.map(x => x.sys_name))];

    $(elem).append(
        '<div class="container">' +
          '<div class="panel-group" id="accord-sysinfo"></div>' +
        '</div>'
    );
    elem = $(elem).find('#accord-sysinfo');

    for (var i = 0; i < system_arr.length; i++) {
        $(elem).append(
            '<div class="panel panel-default">' +
            '<div class="panel-heading" id="accord-' + system_arr[i] + '">' +
              '<h5 class="panel-title">' +
                '<a data-toggle="collapse" data-parent="#accord-sysinfo" href="#accord-col-' + system_arr[i] + '"></a>' +
              '</h5>' +
            '</div>' +
            '<div id="accord-col-' + system_arr[i] + '" class="panel-collapse collapse' + ((i == 0) ? ' in' : '') + '">' +
              '<div class="panel-body">' +
              '</div>' +
            '</div>' +
          '</div>'
        );

        $(elem).find("#accord-" + system_arr[i]).find("a").append("system: " + system_arr[i]);

        sys_elem = $(elem).find("#accord-col-" + system_arr[i]).find(".panel-body");

        //ip_arr = new Set(info.map(x => x.arch).filter(v => "".includes(v))); //x86_64

        x86_64_arr = Array();
        aarch64_arr = Array();
        for (var x = 0; x < info.length; x++) {
            if (info[x]["sys_name"] == system_arr[i]) {
                if (info[x]["arch"] == "x86_64") {
                    x86_64_arr.push(info[x]);
                }
                else if (info[x]["arch"] == "aarch64") {
                    aarch64_arr.push(info[x]);
                }
            }
        }

        $(sys_elem).append(
            "<div class='aarch64'>" +
            "<table class='table'>" + //table-striped
            "<thead>" +
              "<tr>" +
                "<th>arch</th>" +
                "<th>ip</th>" +
                "<th>date</th>" +
                "<th>daemon-app</th>" +
                "<th>aci</th>" +
              "</tr>" +
            "</thead>" +
            "<tbody>" +
            "</tbody>" +
            "</table>" +
            "</div>"
        );

        e = $(sys_elem).find("div.aarch64").find("tbody").last();
        aarch64_arr.sort((a, b) => a.ip.localeCompare(b.ip)).forEach(function(obj) {
            $(e).append("<tr></tr>");
            tr = $(e).find("tr").last();

            $(tr).append("<td>" + obj["arch"] + "</td>");
            $(tr).append("<td>" + obj["ip"] + "</td>");
            $(tr).append("<td>" + (new Date(obj["timestamp"])).toLocaleString("en-US") + "</td>");
            $(tr).append("<td>" + obj["daemon"]["app_version"] + "</td>");
            $(tr).append("<td>" + obj["aci"]["version"] + "</td>");
        });

        $(sys_elem).append(
            "<div class='x86_64'>" +
            "<table class='table'>" + //table-striped
            "<thead>" +
              "<tr>" +
                "<th>arch</th>" +
                "<th>ip</th>" +
                "<th>date</th>" +
                "<th>daemon-app</th>" +
                "<th>daemon-d</th>" +
                "<th>api</th>" +
                "<th>ctools</th>" +
                "<th>asis</th>" +
              "</tr>" +
            "</thead>" +
            "<tbody>" +
            "</tbody>" +
            "</table>" +
            "</div>"
        );

        e = $(sys_elem).find("div.x86_64").find("tbody").first();
        x86_64_arr.sort((a, b) => a.ip.localeCompare(b.ip)).forEach(function(obj) {
            $(e).append("<tr></tr>");
            tr = $(e).find("tr").last();

            $(tr).append("<td>" + obj["arch"] + "</td>");
            $(tr).append("<td>" + obj["ip"] + "</td>");
            $(tr).append("<td>" + (new Date(obj["timestamp"])).toLocaleString("en-US") + "</td>");
            $(tr).append("<td>" + obj["daemon"]["app_version"] + "</td>");
            $(tr).append("<td>" + obj["daemon"]["d_version"] + "</td>");
            $(tr).append("<td>" + obj["api"]["version"] + "</td>");
            $(tr).append("<td>" + obj["ctools"]["version"] + "</td>");
            $(tr).append("<td>" + obj["asis"]["version"] + "</td>");
        });
    }
}

function gen_status_info(info, elem) {
    system_arr = [...new Set(info.map(x => x.sys_name))];

    $(elem).append(
        '<div class="container">' +
          '<div class="panel-group" id="accord-sysinfo"></div>' +
        '</div>'
    );
    elem = $(elem).find('#accord-sysinfo');

    for (var i = 0; i < system_arr.length; i++) {
        $(elem).append(
            '<div class="panel panel-default">' +
            '<div class="panel-heading" id="accord-' + system_arr[i] + '">' +
              '<h5 class="panel-title">' +
                '<a data-toggle="collapse" data-parent="#accord-sysinfo" href="#accord-col-' + system_arr[i] + '"></a>' +
              '</h5>' +
            '</div>' +
            '<div id="accord-col-' + system_arr[i] + '" class="panel-collapse collapse' + ((i == 0) ? ' in' : '') + '">' +
              '<div class="panel-body">' +
              '</div>' +
            '</div>' +
          '</div>'
        );

        $(elem).find("#accord-" + system_arr[i]).find("a").append("system: " + system_arr[i]);

        sys_elem = $(elem).find("#accord-col-" + system_arr[i]).find(".panel-body");

        x86_64_arr = Array();
        aarch64_arr = Array();
        for (var x = 0; x < info.length; x++) {
            if (info[x]["sys_name"] == system_arr[i]) {
                if (info[x]["arch"] == "x86_64") {
                    x86_64_arr.push(info[x]);
                }
                else if (info[x]["arch"] == "aarch64") {
                    aarch64_arr.push(info[x]);
                }
            }
        }

        $(sys_elem).append(
            "<div class='aarch64'>" +
            "<table class='table'>" + //table-striped
            "<thead>" +
              "<tr>" +
                "<th>arch</th>" +
                "<th>ip</th>" +
                "<th>date</th>" +
                "<th>daemon status</th>" +
                "<th>daemon uptime</th>" +
                "<th>compression</th>" +
              "</tr>" +
            "</thead>" +
            "<tbody>" +
            "</tbody>" +
            "</table>" +
            "</div>"
        );

        e = $(sys_elem).find("div.aarch64").find("tbody").last();
        aarch64_arr.sort((a, b) => a.ip.localeCompare(b.ip)).forEach(function(obj) {
            $(e).append("<tr></tr>");
            tr = $(e).find("tr").last();

            $(tr).append("<td>" + obj["arch"] + "</td>");
            $(tr).append("<td>" + obj["ip"] + "</td>");
            $(tr).append("<td>" + (new Date(obj["timestamp"])).toLocaleString("en-US") + "</td>");
            $(tr).append("<td class='" + get_class_name(obj["daemon"]["status"]) + "'>" + obj["daemon"]["status"] + "</td>");
            $(tr).append("<td>" + obj["daemon"]["uptime"] + "</td>");
            $(tr).append("<td>" + obj["aci"]["compression"] + "</td>");
        });

        $(sys_elem).append(
            "<div class='x86_64'>" +
            "<table class='table'>" + //table-striped
            "<thead>" +
              "<tr>" +
                "<th>arch</th>" +
                "<th>ip</th>" +
                "<th>date</th>" +
                "<th>daemon status</th>" +
                "<th>daemon uptime</th>" +
                "<th>asis status</th>" +
                "<th>asis uptime</th>" +
              "</tr>" +
            "</thead>" +
            "<tbody>" +
            "</tbody>" +
            "</table>" +
            "</div>"
        );

        e = $(sys_elem).find("div.x86_64").find("tbody").first();
        x86_64_arr.sort((a, b) => a.ip.localeCompare(b.ip)).forEach(function(obj) {
            $(e).append("<tr></tr>");
            tr = $(e).find("tr").last();

            $(tr).append("<td>" + obj["arch"] + "</td>");
            $(tr).append("<td>" + obj["ip"] + "</td>");
            $(tr).append("<td>" + (new Date(obj["timestamp"])).toLocaleString("en-US") + "</td>");
            $(tr).append("<td class='" + get_class_name(obj["daemon"]["status"]) + "'>" + obj["daemon"]["status"] + "</td>");
            $(tr).append("<td>" + obj["daemon"]["uptime"] + "</td>");
            $(tr).append("<td class='" + get_class_name(obj["asis"]["status"]) + "'>" + obj["asis"]["status"] + "</td>");
            $(tr).append("<td>" + obj["asis"]["uptime"] + "</td>");
        });
    }
}

function get_class_name(status) {
    return (status == "active") ? "green" : "red";
}