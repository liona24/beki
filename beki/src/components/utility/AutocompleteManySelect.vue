<template>
  <b-field :label="label" horizontal>
    <b-field>
      <b-taginput placeholder="..."
        :value="value"

        icon="label"
        field="$repr"

        :data="data"
        :loading="isFetching"
        :required="required"
        :open-on-focus="true"

        @typing="fetchData"

        autocomplete
        expanded>

        <template slot="footer">
          <a class="dropdown-item" @click="launchEditor">
            <b-icon icon="file" size="is-small"></b-icon><span> Hinzufügen ... </span>
          </a>
        </template>
        <template slot="selected" slot-scope="props">
          <div class="tags has-addons" v-for="(tag, index) in props.tags" :key="index">
            <a class="tag is-dark" role="button" :tabindex="false" @click="modifyAt(index)" @keyup.delete.prevent="close">
              <b-icon icon="pencil" size="is-small"></b-icon>
            </a>
            <span class="tag">{{ tag.$repr }}</span>
            <a class="tag is-danger" role="button" :tabindex="false" @click="removeAt(index)" @keyup.delete.prevent="close">
              <b-icon icon="close" size="is-small"></b-icon>
            </a>
          </div>
        </template>
      </b-taginput>
      <p class="control">
        <button class="button" @click="launchEditor"><b-icon icon="file" ></b-icon></button>
      </p>
    </b-field>
  </b-field>
</template>

<script>
import { SyncStatus } from '../../store/common'
import { debounce, cloneDeep } from 'lodash'

export default {
  name: "AutocompleteManySelect",
  props: {
    required: {
      type: Boolean,
      default: false
    },
    label: String,
    endpoint: String,
    value: Object,

    create: Function,
    update: String,
    remove: String,
  },
  data() {
    return {
      data: [],
      isFetching: false,
      currentInput: "",
    }
  },
  methods: {
    fetchData: debounce(function(query) {
      this.isFetching = true;
      this.currentInput = query;

      console.log("Fetching from ", this.endpoint);
      // TODO: fetch actual autocompletions
      setTimeout(() => this.isFetching = false, 500);
    }, 500),
    launchEditor() {
      const obj = this.create(this.currentInput);
      obj.$status = SyncStatus.New;

      this.$store.commit("push", {
        view: obj,
        callback: this.update,
        args: {
          i: -1
        }
      });
    },
    removeAt(index) {
      console.log("TODO remove", index);
      this.$store.commit(this.remove, index);
    },
    modifyAt(index) {
      console.log("TODO modify", index);
      const obj = cloneDeep(this.value[index]);
      this.$store.commit("push", {
        view: obj,
        callback: this.update,
        args: {
          i: index
        }
      });
    }
  }

}
</script>

<style>

</style>
