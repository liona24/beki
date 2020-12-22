<template>
  <b-field :label="label" horizontal>
    <b-field>
      <b-taginput placeholder="..."
        :value="value"
        @add="addValue"

        icon="tags"
        field="$repr"

        :data="filteredData"
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
            <a class="tag is-danger" role="button" :tabindex="false" @click="removeAt(index)" @keyup.delete.prevent="close">
              <b-icon icon="times" size="is-small"></b-icon>
            </a>
            <span class="tag">{{ tag.$repr }}</span>
            <a class="tag is-dark" role="button" :tabindex="false" @click="modifyAt(index)" @keyup.delete.prevent="close">
              <b-icon icon="edit" size="is-small"></b-icon>
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

    requestSrc: String,

    value: Array,

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
  computed: {
    filteredData() {
      return this.data.filter(record =>
        this.value.find(val =>
          val.id === record.id) === undefined
      );
    }
  },
  methods: {
    addValue(e) {
      this.$store.commit(this.update, {
        val: e,
        i: -1
      });
    },
    fetchData: debounce(function(query) {
      if (query.length < 1) {
        this.data = [];
        return;
      }

      this.isFetching = true;
      this.currentInput = query;

      this.$http.post("api/_discover", {
          q: query,
          src: this.requestSrc,
      }).then(resp => {
        this.data = resp.body;
      }, () => {
        console.error("discover api unavailable");
      }).finally(() => {
        this.isFetching = false;
      });
    }, 500),
    launchEditor() {
      const obj = this.create(this.currentInput);
      obj.$status = SyncStatus.New;

      this.$store.commit("push_overlay", {
        view: obj,
        callback: this.update,
        args: {
          i: -1
        }
      });
    },
    removeAt(index) {
      this.$store.commit(this.remove, index);
    },
    modifyAt(index) {
      const obj = cloneDeep(this.value[index]);
      this.$store.commit("push_overlay", {
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
