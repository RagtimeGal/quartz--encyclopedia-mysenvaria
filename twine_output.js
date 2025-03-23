switch (input) {
  case "ping":
    SugarCube.State.variables.context = "ichor";
    changeBackground("ichor.png");
    if (context === "you") {
      response = "Pong. <span style="color:aqua">Ichor.</span>";
      break;
    }
    break;
  case "ping":
    SugarCube.State.variables.context = "you";
    changeBackground("you.png");
    if (context === "ichor") {
      response = "Pong. <span style="color:aqua">Overseer.</span>";
      break;
    }
    break;
  default:
    response = "I do not understand that question.";
    break;
}