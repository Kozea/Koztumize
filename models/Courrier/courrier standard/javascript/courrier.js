$(function () { 
  var civ = ['Madame, Monsieur', 'Madame', 'Monsieur'];
  var sal = ['Cordialement', 'Veuillez agréer mes salutations distinguées'];
  
    $('.civilites').hover(function(){
      if(!$(this).text()){      
        $(this).html($('<ul></ul>').addClass("civiliste"));
        $.each(civ, function(i, val){$('.civiliste').append('<li>'+val+'</li>')});
      }
    }, function () {
        $(this).find('.civiliste').remove();
      });
    
     $('.salutation').hover(function(){
      if(!$(this).text()){      
        $(this).html($('<ul></ul>').addClass("salutaliste"));
        $.each(sal, function(i, val){$('.salutaliste').append('<li>'+val+'</li>')});
      }
    }, function () {
        $(this).find('.salutaliste').remove();
      });
  
  $('.civilites').on('click', '.civiliste li', function(){
    $('.civilites').html($(this).html());
    sal.push('Veuillez agréer, '+$('.civilites').html()+', mes sincères salutations');
  });
  
  $('.salutation').on('click', '.salutaliste li', function(){
    $('.salutation').html($(this).html());
  });
      
  if($('#date').is(':empty')) $('#date').html(getCurrentDate());
  if($('.signature').is(':empty')) $('.signature').html($('meta[name=author]').attr('content'));
  
  
  $('div[contenteditable=true]').dblclick(function(){
    document.execCommand('selectall',false,'');
  });
});

    
function getCurrentDate(){
  var mois = ['Janvier','Février','Mars','Avril','Mai','Juin','Juillet','Août','Septembre','Octobre','Novembre','Décembre'];
  var date=new Date();
  return 'le ' + date.getDate() + ' ' + mois[date.getMonth()] + ' ' + date.getFullYear();
}
    
