<template>
  <div class="image-container">
    <figure class="image">
        <img :src="url" class="is-rounded" style="border-radius: .3em" />
    </figure>
    <div class="delete-overlay">
      <a @click="remove"><b-icon tag="a" icon="trash" size="is-medium" type="is-white"></b-icon></a>
    </div>
  </div>
</template>

<script>
export default {
  name: "RemovableImage",
  props: {
    url: String
  },
  methods: {
    remove() {
      this.$emit("remove");
    }
  }
}
</script>

<style scoped>

.image-container {
  position: relative;
  display: flex;
  justify-content: center;
  min-width: 128px;
}
.delete-overlay {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  height: 100%;
  width: 100%;
  opacity: 0;
  border-radius: 0.3em;
  transition: 0.3s ease;
  background-color: rgba(0, 0, 0, 0.7);
}

.image-container:hover .delete-overlay {
  opacity: 1;
}

.image-container .icon {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  -ms-transform: translate(-50%, -50%);
  text-align: center;
}

</style>
