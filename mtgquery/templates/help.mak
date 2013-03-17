<%! import mtgquery.templates.util.common_js as common_js %>
<%inherit file="base.mak"/>
<div class="well well-small container">
  ${contents |n}
</div>
<%block name="js_onready">${common_js.card_tooltips() |n}</%block>
