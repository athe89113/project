<template>
  <div style="margin-top: 5px">
    <message :message-type="message_type"></message>
  </div>
</template>


<script>
  import message from './message.vue'
  export default {
    data: function () {
      return {
        message_type: "assets"
      }
    },
    ready: function () {
    },
    methods:{
    },
    components: {
      message
    }
  }
</script>