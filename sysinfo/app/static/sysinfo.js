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

function gen_x86_64_info(e, info) {
    $(e).append("<tr></tr>");
    tr = $(e).find("tr").last();

    $(tr).append("<td>" + info["arch"] + "</td>");
    $(tr).append("<td>" + info["ip"] + "</td>");
    $(tr).append("<td>" + (new Date(info["timestamp"])).toLocaleString("en-US") + "</td>");
    $(tr).append("<td>" + info["daemon"]["app_version"] + "</td>");
    $(tr).append("<td>" + info["daemon"]["d_version"] + "</td>");
    $(tr).append("<td>" + info["api"]["version"] + "</td>");
    $(tr).append("<td>" + info["ctools"]["version"] + "</td>");
    $(tr).append("<td>" + info["asis"]["version"] + "</td>");
}

function gen_aarch64_info(e, info) {
    $(e).append("<tr></tr>");
    tr = $(e).find("tr").last();

    $(tr).append("<td>" + info["arch"] + "</td>");
    $(tr).append("<td>" + info["ip"] + "</td>");
    $(tr).append("<td>" + (new Date(info["timestamp"])).toLocaleString("en-US") + "</td>");
    $(tr).append("<td>" + info["daemon"]["app_version"] + "</td>");
    $(tr).append("<td>" + info["aci"]["version"] + "</td>");

}

function gen_info(info, elem) {
    system_arr = [...new Set(info.map(x => x.sys_name))];

    for (var i = 0; i < system_arr.length; i++) {
        $(elem).append(
            "<div class='container " + system_arr[i] + "'>" +
            "<p class='system'>system: " + system_arr[i] + "</p>" +
            "</div>"
        );

        sys_elem = $(elem).find("div." + system_arr[i]);

        $(sys_elem).append(
            "<div class='container x86_64'>" +
            "<table class='table table-striped'>" +
            "<thead>" +
              "<tr>" +
                "<th>arch</th>" +
                "<th>ip</th>" +
                "<th>date</th>" +
                "<th>daemon-app</th>" +
                "<th>daemon-daemon</th>" +
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

        //ip_arr = new Set(info.map(x => x.arch).filter(v => "".includes(v))); //x86_64
        arch_arr = new Set(info.map(x => x.arch));

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

        e = $(sys_elem).find("div.x86_64").find("tbody").first();
        for (var j = 0; j < x86_64_arr.length; j++) {
            gen_x86_64_info(e, x86_64_arr[j]);
        }

        $(sys_elem).append(
            "<div class='container aarch64'>" +
            "<table class='table table-striped'>" +
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
        for (var j = 0; j < aarch64_arr.length; j++) {
            gen_aarch64_info(e, aarch64_arr[j]);
        }
    }
}