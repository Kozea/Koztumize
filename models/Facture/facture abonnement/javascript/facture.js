function Calculate(){  
  var len = $('table.table tbody tr').length;
  var $tot = 0;
  var $tot_tva = 0;
  for(var i=0; i<len ; i++){
    var $qte = $('table.table tbody tr:eq('+i+') td:eq(1) span').html(); 
    var $puht = new Number($('table.table tbody tr:eq('+i+') td:eq(2) span').html());
    $('table.table tbody tr:eq('+i+') td:eq(2) span').html($puht.toFixed(2));
    var $tot_ht = $qte*$puht;
    /* remplit la case total HT par qte*prix unitaire HT */
    $('table.table tbody tr:eq('+i+') td:eq(3)').html($tot_ht.toFixed(2)+' €');
    $tot +=  $tot_ht;
    var $tva = $('table.table tbody tr:eq('+i+') td:eq(4) span').html().replace(',','.');
    $tot_tva += ($tva*$tot_ht)/100;
  }
  
  $('table.total tbody tr td:eq(0)').html($tot_tva.toFixed(2)+' €'); 
  $('table.total tbody tr td:eq(1)').html($tot.toFixed(2)+' €');
  var $tot_ttc = $tot_tva + $tot;
  $('table.total tbody tr td:eq(2)').html($tot_ttc.toFixed(2)+' €'); 
}

function AddLine(){
  $('table.table tbody').append('<tr><td><div class="first last"><div contenteditable="true" class="" title=""></div></div></td><td><span contenteditable="true">1</span></td><td><span contenteditable="true">0</span>&nbsp;€</td><td>&nbsp;</td><td><span contenteditable="true">19,6</span>&nbsp;%</td></tr>');
}

function RemLine(){
  $('table.table:eq(0) tbody tr:last').remove();
  replaceComma();
  Calculate();
  replaceDot();
}

function replaceDot(){
  $('table.table tbody tr td:not(table.table tbody tr td:first-child),table.total tbody tr td').each(function() {
    var value = $(this).html();
    $(this).html(value.replace('.',','));
  });
}

function replaceComma(){
  $('span[contenteditable=true]').each(function() {
    var value = $(this).html();
    $(this).html(value.replace(',','.'));
  });
}

function getCurrentDate(){
  var mois = ['Janvier','Février','Mars','Avril','Mai','Juin','Juillet','Août','Septembre','Octobre','Novembre','Décembre'];
  var date=new Date();
  return 'le ' + date.getDate() + ' ' + mois[date.getMonth()] + ' ' + date.getFullYear();
}
   
$(function () {
    $("table.table").on('blur', "span[contenteditable=true]", function () { replaceComma(); Calculate(); replaceDot(); });
    if($('#date').is(':empty')) $('#date').html(getCurrentDate());
    
    var type = ['Facture','Devis'];
    var regl = ['Virement bancaire','Chèque','Prélèvement bancaire','Espèces'];
    
    $('.type').hover(function(){
      if(!$(this).text()){      
        $(this).html($('<ul></ul>').addClass("typeliste"));
        $.each(type, function(i, val){$('.typeliste').append('<li>'+val+'</li>')});
      }
     }, function () {
        $(this).find('.typeliste').remove();
    });
    
    $('.reglement').hover(function(){
      if(!$(this).text()){      
        $(this).html($('<ul></ul>').addClass("regliste"));
        $.each(regl, function(i, val){$('.regliste').append('<li>'+val+'</li>')});
      }
    }, function () {
        $(this).find('.regliste').remove();
    });
      
    $('.type').on('click', '.typeliste li', function(){
      $('.type').html($(this).html());
    });
    
    $('.reglement').on('click', '.regliste li', function(){
      $('.reglement').html($(this).html());
    });
});

