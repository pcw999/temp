<template>
    <button v-on:click="click_a">check</button>
</template>
<script>

export default {
    methods: {
        click_a() {
            const spawn = require('child_process').spawn;

            const result = spawn('python', ['./src/python/count.py']);

            result.stdout.on('data', function (data) {
                console.log(data.toString());
            });

            result.stderr.on('data', function (data) {
                console.log(data.toString());
            });
        }
    }
}

</script>