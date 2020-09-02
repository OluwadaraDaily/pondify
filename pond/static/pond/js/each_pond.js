// document.addEventListener('DOMContentLoaded', () => {
	
	// document.getElementById("refresh").onclick = () => {
	async function refresh() {
		// get URL and hence channel ID
		const api_url = new URL (window.location.href);
		const n = api_url.pathname.length;
		const channel_id = api_url.pathname.substring(1,n);

		// const Http = new XMLHttpRequest();
		
		const url='https://api.thingspeak.com/channels/' + channel_id +'/feeds.json?api_key=Z7POUDWMQBPRKQU1&results=1';
		// console.log(url);
		// Http.open("GET", url, false);
		// Http.send();

		let response = await fetch(url)
		let data = JSON.parse(await response.text())

		// Http.onreadystatechange = (e) => {
		// res = JSON.parse(Http.responseText);
		document.getElementById("temp").value = data.feeds[0].field1;
		document.getElementById("ph").value = data.feeds[0].field2;
		document.getElementById("water_level").value = data.feeds[0].field4;
		// console.log(data)
		// }
	}	
// }
		
// });