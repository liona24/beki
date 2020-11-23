<template>
  <b-loading v-if="isLoading" v-model="isLoading" :is-full-page="true" :can-cancel="false"></b-loading>
  <div v-else>
      <div class="box">
        <status-indicator type="is-warning" content="Status"></status-indicator>
        <editor-protocol-header />
      </div>
      <div class="box">
        <status-indicator type="is-warning" content="Status">
          <a class="tag delete is-danger" slot="left" @click="removeEntry(0)"></a>
        </status-indicator>
        <editor-entry />
      </div>
  </div>
</template>

<script>
import EditorProtocolHeader from './EditorProtocolHeader.vue'
import EditorEntry from './EditorEntry.vue'
import StatusIndicator from '../utility/StatusIndicator'

export default {
  components: { EditorProtocolHeader, EditorEntry, StatusIndicator },
  name: "Editor",
  data() {
    return {
      isLoading: false,
      entries: []
    }
  },
  methods: {
    removeEntry(i) {
      console.log(i);
    }
  }

}
</script>

<style>

</style>
