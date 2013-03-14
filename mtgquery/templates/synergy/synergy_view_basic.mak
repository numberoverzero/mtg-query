<%inherit file="../components/bootstrap.mak"/>
<%namespace name="base" file="../components/base.mak"/>
<%namespace name="raw" file="synergy_view_data.mak"/>

<div class="row-fluid">
  <div class="span10 offset1">
    ${raw.render(name, description, counts, urls, link_alt_href, 'Full View', new_link_href=copy_from_href)}
  </div>
  <div class="span1"/>
</div>

<%def name="js()">
${parent.js()}
</%def>

<%def name="css()">
${parent.css()}
${base.css_link('/css/mtgquery.css', 'screen')}
</%def>

<%def name="js_onready()">
${parent.js_onready()}
${raw.js_onready()}
</%def>