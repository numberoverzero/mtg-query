(function( $ ){

  $.fn.notifier = function (max_notifications){
      var self = this;
      self.template = $(
      '<div class="notification alert alert-error">' +
        '<h4 class="alert-heading" />' +
      '</div>');
      
      self.active = 0;
      self.max = max_notifications;
      self.queue = [];
      self.has_pending = function() { return self.queue.length > 0; };
      self.notification_area = this;
      
      self.close = function(){
          $(this).slideUp("slow");
          self.active--;
          
          if(self.active < self.max && self.has_pending()){
              self.add(self.queue.shift());
          }
          else {
              self.update();
          }
      };
      
      self.close_all = function(){
          self.active = 0;
          self.queue.length = 0;
          $('div.notification').slideUp("normal");
          self.update();
      };
      
      self.update = function(){
          self.queued_alert.find('.alert-heading').text("... and " + self.queue.length + " more");
          if(self.has_pending()){
              self.queued_alert.slideDown("slow");
              self.queued_alert.appendTo(self.notification_area);
          }
          else {
              self.queued_alert.hide();
          }
      };
      
      self.add = function (msg) {
          if(self.max > 0 && self.active >= self.max){
              self.queue.push(msg);
          }
          else {
              self.active++;
              var $n = self.template.clone().appendTo(self.notification_area);
              msg = _.unescape(msg);
              msg = msg.replace(/&#34;/g, "\"");
              msg = msg.replace(/&#39;/g, "'");
              $n.find('.alert-heading').text(msg);
              $n.hide().slideDown("slow");
              $n.click(self.close);
          }
          self.update();
      };
      
      self.queued_alert = self.template.clone();
      self.queued_alert.click(self.close_all);
      
      return self.add;
  };
})( jQuery );
