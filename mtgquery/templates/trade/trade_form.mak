<%!
  import mtgquery.templates.util.common_js as common_js
  from mtgquery.templates.util.util import ifelse

  def jquery_bool(var):
    return 'true' if var else 'false'
%>
<%namespace name="base" file="../components/base.mak"/>
<%def name="form(title, name='', stack_1_text='', stack_2_text='')">
<% name = ifelse(name is None, '', name) %>
<form id="trade-form" class="well form-center" action="#" method="POST">
  <fieldset>
    <legend>
      ${title}
      <div class="pull-right">
        <a id="help-button" href="/help/site#trade" class="btn btn-primary btn-default">Help</a>
      </div>
    </legend>
    <div class="control-group">
      <label class="control-label" for="trade-name">Name</label>
      <div class="controls">
        <input class="text input-xlarge" id="trade-name" name="trade-name" placeholder="(optional)" value="${name |n}" />
      </div>
    </div>
    <div class="control-group">
      <label class="control-label" for="card-stack-1">Stack One</label>
      <div class="controls">
        <textarea class="input-xlarge" id="card-stack-1" name="card-stack-1" placeholder="4 Black Lotus" rows="6">${stack_1_text |n}</textarea>
      </div>
    </div>
    <div class="control-group">
      <label class="control-label" for="card-stack-2">Stack Two</label>
      <div class="controls">
        <textarea class="input-xlarge" id="card-stack-2" name="card-stack-2" placeholder="Time Walk" rows="6">${stack_2_text |n}</textarea>
      </div>
    </div>
    <div class="control-group">
      <label class="control-label" for="price-source">Source</label>
      <div class="controls">
        <select id="price-source" name="price-source">
          <option value="tcgplayer">TCGPlayer</option>
        </select>
      </div>
    </div>
    <div class="control-group">
      <label class="control-label" for="use-cached">Cached Prices</label>
      <div class="controls">
        <div id="cache-toggle-button">
          <input type="checkbox" checked="checked" id="use-cached" name="use-cached" />
        </div>
      </div>
    </div>
    <div class="form-actions">
      <button type="submit" class="btn btn-primary btn-large">Compare</button>
    </div>
  </fieldset>
</form>
</%def>

<%def name="form_preload_settings(source_value, use_cached)">
$("#price-source").val("${source_value}");
$('#cache-toggle-button').toggleButtons('setState', ${jquery_bool(use_cached)});
</%def>

<%def name="form_css()">
${base.css_link('/css/bootstrap-toggle-buttons.css', 'screen')}
</%def>

<%def name="form_js()">
${base.js_script("/js/jquery.autosize-min.js")}
${base.js_script("/js/bootstrap-toggle-buttons.js")}
${base.js_script("/js/trade-toggle-buttons.js")}
</%def>

<%def name="form_js_onready()">
${common_js.autosize('textarea') |n}
</%def>