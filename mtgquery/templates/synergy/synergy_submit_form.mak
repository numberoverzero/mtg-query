<%!
  import mtgquery.templates.util.common_js as common_js

  def jquery_bool(var):
    return 'true' if var else 'false'
%>
<%namespace name="base" file="../components/base.mak"/>
<%def name="form(title, name='', description='', cards_text='')">
<form id="synergy-form" class="well form-center" action="#" method="POST">
  <fieldset>
    <legend>
      ${title}
      <div class="pull-right">
        <a id="help-button" href="/help/site#synergy" class="btn btn-primary btn-default">Help</a>
      </div>
    </legend>
    <div class="control-group">
      <label class="control-label" for="synergy-name">Name</label>
      <div class="controls">
        <input class="text input-xlarge" id="synergy-name" name="synergy-name" placeholder="(optional)" value="${name |n}" />
      </div>
    </div>
    <div class="control-group">
      <label class="control-label" for="synergy-description">Description</label>
      <div class="controls">
        <textarea class="input-xlarge" id="synergy-description" name="synergy-description" placeholder="(optional)" rows="6">${description |n}</textarea>
      </div>
    </div>
    <div class="control-group">
      <label class="control-label" for="synergy-cards">Cards</label>
      <div class="controls">
        <textarea class="input-xlarge" id="synergy-cards" name="synergy-cards" placeholder="9001 Forest" rows="6">${cards_text |n}</textarea>
      </div>
    </div>
    <div class="form-actions">
      <button type="submit" class="btn btn-primary btn-large">Synergize!</button>
    </div>
  </fieldset>
</form>
</%def>

<%def name="form_js()">
${base.js_script("/js/jquery.autosize-min.js")}
</%def>

<%def name="form_js_onready()">
${common_js.autosize('textarea') |n}
</%def>