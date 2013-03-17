<%inherit file="../mtgquery_base.mak"/>
<%namespace name="base" file="../components/base.mak"/>
<%namespace name="raw" file="synergy_view_data.mak"/>
<%def name="body()">
${parent.body()}
<div class="well well-small container">
% for synergy in synergies:
  <a href="${synergy['url']}">
  <div class="well">
    <h3>${synergy['name']}</h3>
    <span>${synergy['length']} cards</span>
  </div>
  </a>
% endfor
</div>
</%def>

<%def name="css()">
${parent.css()}
</%def>

<%def name="js()">
${parent.js()}
</%def>

<%def name="js_onready()">
${parent.js_onready()}
</%def>