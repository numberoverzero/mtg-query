<%inherit file="../mtgquery_base.mak"/>
<%namespace name="base" file="../components/base.mak"/>
<%namespace name="raw" file="synergy_view_data.mak"/>
<%def name="body()">
${parent.body()}
<div class="well well-small container">
    <h2>No results for 'Search'</h2>
    <hr>
    <p>Sorry about that!  Search is still being built.</p>
    <p>Eventually, search will let you find synergies based on a host of criteria, including (ideally) most of the criteria available on the gatherer website, as well as the inclusion or exclusion of specific cards.</p>
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