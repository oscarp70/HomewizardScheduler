<head>
    <title>Beregening</title>
    <meta name="viewport" content="width=device-width; initial-scale=1.0; maximum-scale=1.0;">
    <link rel="icon" href="{{url_for('static',filename='drop.png')}}"></link>
    <link rel="stylesheet" type="text/css" href="{{url_for('static',filename='styles.css')}}"> media="screen"/>
<style>
.slidecontainer {
  width: 100%;
}
div.sticky {
  position: -webkit-sticky; /* Safari */
  position: sticky;
  top: 0;
  background-color: CornflowerBlue;
  padding: 0px;
  text-align: center;
  font-size: 32px;
}

div.labels {
  text-align: center;
  font-size: 24px;

}
</style>
<style>
.block {
  display: block;
  width: 100%;
  border: none;
  background-color: CornflowerBlue;
  padding: 14px 28px;
  font-size: 24px;
  cursor: pointer;
  text-align: center;
}
.slider {
  -webkit-appearance: none;
  width: 100%;
  height: 55px;
  background: #d3d3d3;
  outline: none;
  opacity: 0.7;
  -webkit-transition: .2s;
  transition: opacity .2s;
}

.slider:hover {
  opacity: 1;
}

.slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 55px;
  height: 55px;
  background: #4CAF50;
  cursor: pointer;
}

.slider::-moz-range-thumb {
  width: 55px;
  height: 55px;
  background: #4CAF50;
  cursor: pointer;
}
input[type='checkbox'] {
    -webkit-appearance:none;
    width:30px;
    height:30px;
    background:white;
    border-radius:5px;
    border:2px solid #555;
}
input[type='checkbox']:checked {
    background: #000;
}
</style>

</head>
<body>

<div id="page_wrapper">
<div class="sticky">Beregening</div>    
<form action="/timer/" method="post">
<p>
<div class="slidecontainer">
<div class="labels">Uren:  <span id="uren_waarde"></span></div>
<input type="range" name="uren" class="slider" id="uren" list="uren_list"
  step="1" min="0" max="5">
<datalist id="uren_list">
  <option>0</option>
  <option>1</option>
  <option>2</option>
  <option>3</option>
  <option>4</option>
  <option>5</option>
</datalist>
</div>

<script>
var slider = document.getElementById("uren");
var output = document.getElementById("uren_waarde");
output.innerHTML = slider.value;

slider.oninput = function() {
  output.innerHTML = this.value;
}
</script>

<div class="slidecontainer">
<div class="labels">Minuten: <span id="minuten_waarde"></span></div>
<input type="range" name="minuten" class="slider" id="minuten" list="minuten_list"
  step="10" min="0" max="50">
<datalist id="minuten_list">
  <option>0</option>
  <option>10</option>
  <option>20</option>
  <option>30</option>
  <option>40</option>
  <option>50</option>
</datalist>
</div>    
</p>

<script>
var slider2 = document.getElementById("minuten");
var output2 = document.getElementById("minuten_waarde");
output2.innerHTML = slider2.value;

slider2.oninput = function() {
output2.innerHTML = this.value;
}
</script>

<div class="labels">Pomp aan </div>
<center><input type="checkbox" id="pompAan" name="pompAan" value="pompAan"></center>
<br>
<button name="scheduleBtn" type="submit" class="block">Timer activeren</button>
</form>
   
</div>

</body>

