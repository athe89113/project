<template>
  <div class="ys-box">
    <div class="ys-box-con">
      <div style="margin-top: 5px">
        <message :message-type="message_type"></message>
      </div>
    </div>
  </div>

</template>


<script>
  import message from './message.vue'
  export default {
    data: function () {
      return {
        message_type: "security"
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