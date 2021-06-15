$(function(){
	$(".hamburger").on("click", function(){
		$(this).toggleClass("is-active");
		$(".menu").toggleClass("is-active-menu");
	});
});
