// This file is part of InvenioRDM
// Copyright (C) 2021 TU Wien.
//
// Invenio Theme TUW is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

document.addEventListener("DOMContentLoaded", function () {
  var _paq = (window._paq = window._paq || []);

  /* tracker methods like "setCustomDimension" should be called before "trackPageView" */
  _paq.push(["trackPageView"]);
  _paq.push(["enableLinkTracking"]);

  (function () {
    var u = document.getElementById("matomo-url").value;
    var siteId = document.getElementById("matomo-site-id").value;

    _paq.push(["setTrackerUrl", u + "matomo.php"]);
    _paq.push(["setSiteId", siteId]);

    var d = document;
    var g = d.createElement("script");
    var s = d.getElementsByTagName("script")[0];

    g.type = "text/javascript";
    g.async = true;
    g.src = u + "matomo.js";
    s.parentNode.insertBefore(g, s);
  })();
});
