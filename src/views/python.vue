<template>
  <div class="about">
    <h1>This is an about page</h1>
  </div>
</template>

<script>
const { PythonShell } = require("python-shell");
let options = {
  scriptPath: "./src/views",
  args: ['value1', 'value2', 'value3']
};
PythonShell.run("my_script.py", options, function (err, data) {
  if (err) throw err;
  console.log(data);
});
</script>                    