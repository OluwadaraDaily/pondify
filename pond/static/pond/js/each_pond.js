document.addEventListener('DOMContentLoaded', () => {
	
	document.getElementById("refresh").onclick = () => {

		// get URL and hence channel ID
		const api_url = new URL (window.location.href);
		const n = api_url.pathname.length;
		const channel_id = api_url.pathname.substring(1,n);

		const Http = new XMLHttpRequest();
		
		const url='https://api.thingspeak.com/channels/' + channel_id +'/feeds.json?results=1';
		Http.open("GET", url);
		Http.send();

		Http.onreadystatechange = (e) => {
			res = JSON.parse(Http.responseText);
			document.getElementById("temp").value = res.feeds[0].field1;
			document.getElementById("ph").value = res.feeds[0].field2;
		}
	}
});