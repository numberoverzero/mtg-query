<%inherit file="../components/bootstrap.mak"/>
<%namespace name="base" file="../components/base.mak"/>
<%namespace name="raw" file="trade_raw.mak"/>

<div class="row-fluid">
  <div class="span10 offset1">
    ${raw.render(name, data_1, data_2, gt_1, gt_2, diff, headers, link_alt_href, 'Full View')}
  </div>
  <div class="span1"/>
</div>

<%def name="css()">
${parent.css()}
${raw.render_css()}
${base.css_link('/css/mtgquery.css', 'screen')}
</%def>

<%def name="js()">
${parent.js()}
${raw.render_js()}
</%def>

<%def name="js_onready()">
${parent.js_onready()}
${raw.render_js_onready()}
</%def>