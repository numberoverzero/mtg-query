<%!
    import mtgquery.templates.util.common_js as common_js
%>
<%inherit file="../mtgquery_base.mak"/>
<%namespace name="components" file="../components/components.mak"/>
<%namespace name="base" file="../components/base.mak"/>
<%namespace name="form" file="trade_form.mak"/>
<%namespace name="raw" file="trade_raw.mak"/>
<%def name="body()">
${parent.body()}
<div class="row-fluid">
  <div class="span2"></div>
  <div class="span8">
    <div id="notification-area"></div>
  </div>
  <div class="span2" />
</div>

<div class="row-fluid">  
  <div class="span1"></div>
  <div class="span6">
    ${raw.render(name, data_1, data_2, gt_1, gt_2, diff, headers, link_alt_href, 'Basic View')}
  </div>
  <div class="span4">
    ${form.form("Copy to New", form_name, form_stack_1_text, form_stack_2_text)}
  </div>
  <div class="span1" />
</div>
</%def>

<%def name="css()">
${parent.css()}
${form.form_css()}
${raw.render_css()}
</%def>

<%def name="js()">
${parent.js()}
${raw.render_js()}
${form.form_js()}
% if len(notifications) > 0:
${base.js_script("/js/jquery.notifier.js")}
% endif
</%def>

<%def name="js_onready()">
${parent.js_onready()}
${raw.render_js_onready() |n}
${form.form_js_onready() |n}
${form.form_preload_settings(form_source_value, form_use_cached) |n}
% if len(notifications) > 0:
${common_js.notifier_init("notify", "notification-area", 3, notifications=(n.msg for n in notifications)) |n }
% endif
</%def>