<%inherit file="base.mak"/>
<div class="well well-small container">
  ${contents |n}
</div>
<%block name="js_onready">
var tt = $("a.card-tooltip[rel=tooltip]");
tt.tooltip({
    html: true,
    trigger: 'click',
    placement: 'right',
    animation: false,
    template: '<div class="tooltip"><div class="tooltip-inner"></div></div>'}).click(function(e) { e.preventDefault();
});
tt.tooltip('show');
tt.tooltip('hide');
</%block>
