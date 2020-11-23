<template>
  <nav class="level">
    <div class="level-left">
      <slot name="left"></slot>
    </div>
    <div class="level-right">
      <div class="level-item">
        <b-tag :type="type">
          <slot>
            {{ content }}
          </slot>
        </b-tag>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: "StatusIndicator",
  props: {
    type: String,
    content: {
      type: String,
      default: ""
    }
  }
}
</script>

<style>

</style>
