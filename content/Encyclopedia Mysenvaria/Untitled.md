<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Timeline</title>
<style>
  body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
  }
  .timeline {
    list-style: none;
    padding: 0;
  }
  .event {
    margin-bottom: 20px;
    padding-left: 20px;
    position: relative;
  }
  .event:before {
    content: '';
    position: absolute;
    left: -10px;
    top: 5px;
    width: 10px;
    height: 10px;
    background-color: #333;
    border-radius: 50%;
  }
  .event:last-child {
    margin-bottom: 0;
  }
  .date {
    font-weight: bold;
    margin-bottom: 5px;
  }
  .description {
    margin-left: 10px;
  }
</style>
</head>
<body>

<ul class="timeline">
  <li class="event">
    <div class="date">2020</div>
    <div class="description">Event description goes here.</div>
  </li>
  <li class="event">
    <div class="date">2021</div>
    <div class="description">Event description goes here.</div>
  </li>
  <li class="event">
    <div class="date">2022</div>
    <div class="description">Event description goes here.</div>
  </li>
  <!-- Add more events as needed -->
</ul>

</body>
</html>
