<template>
  <main id="app">
    <section class="section">
      <div class="container">
        <form @submit.prevent="searchKeyword()">
          <div class="field has-addons">
            <div class="cotrol is-expanded">
              <input class="input" type="text" v-model="keyword"/>
            </div>
            <div class="control">
              <button type="form" class="button is-info">
                検索
              </button>
            </div>
          </div>
        </form>
      </div>
    </section>
    <section class="section" v-if="list">
      <div class="container">
        <p id="search-top">{{hit}}件見つかりました。</p>
        <b-pagination v-if="!selected && !selectedTag" :total="hit" :current.sync="page" :per-page="size" @change="pageChange">
        </b-pagination>
        <div v-if="selected">
          {{selected.title}}に似ている本：
        </div>
        <div v-if="selectedTag">
          <b-tag type="is-dark">{{ndcLabel[selectedTag]}}</b-tag>の本
        </div>
        <div v-if="selectedAuthor">
          <b-tag type="is-dark">{{selectedAuthor}}</b-tag>の本
        </div>
        <div v-if="selectedPublisher">
          <b-tag type="is-dark">{{selectedPublisher}}</b-tag>の本
        </div>
        <hr />

        <article class="media" v-for="doc in list" :key=doc.id>
         <div class="media-content">
           <div class="content">
             <p>
               <strong><a :href="'https://dl.ndl.go.jp/info:ndljp/pid/'+doc.id">{{doc.title}}</a></strong>({{doc.publsihed}})
               <br />
               <b-tag @click.native="searchAuthor(doc.responsibility)">{{doc.responsibility}}</b-tag>
               <b-tag @click.native="searchPublisher(doc.publisher)">{{doc.publisher}}</b-tag>
               <br />
               <b-taglist>
                 <b-tag class="search-tag" v-for="tag in doc.tags" :key="tag.id" type="is-dark" @click.native="searchTag(tag)">{{ndcLabel[tag]}}</b-tag>
               </b-taglist>
               {{doc.index}}
             </p>
           </div>
         </div>
         <div class="media-right">
           <button class="button" @click="searchSimilar(doc)">
             この本に似た本を探す
           </button>
         </div>
       </article>
     </div>
   </section>
   <b-loading :is-full-page="true" :active.sync="isLoading"></b-loading>
 </main>
</template>

<script>
import VueScrollTo from 'vue-scrollto';
const searchUrl = 'http://localhost:9200/structuring_knowledge/_search';

export default {
  name: 'App',
  data() {
    return {
      keyword: '',
      list: null,
      hit: 0,
      page: 1,
      size: 20,
      isLoading: false,
      selected: null,
      selectedTag: null,
      selectedAuthor: null,
      selectedPublisher: null,
      ndcLabel: {}
    };
  },
  async mounted() {
    const response = await fetch('https://raw.githubusercontent.com/vopaldragon/knstr/master/ndc.json');
    this.ndcLabel = await response.json();
  },
  methods: {
    pageChange(newPage) {
      this.page = newPage;
      this.search();
    },
    searchKeyword() {
      this.page = 1;
      this.search();
    },
    async search() {
      const from = (this.page - 1) * this.size;
      const query = {
        query: { match: { keywords: this.keyword } },
        from: from,
        size: this.size
      };
      this.isLoading = true;
      this.selected = null;
      this.selectedTag = null;
      this.selectedAuthor = null;
      this.selectedPublisher = null;
      const response = await fetch(searchUrl, {
        method: 'POST',
        headers: {
          "Content-Type": "application/json; charset=utf-8"
        },
        body: JSON.stringify(query)
      });
      const json = await response.json();
      this.list = json.hits.hits.map(doc => doc._source);
      this.hit = json.hits.total.value;
      this.isLoading = false;
    },
    searchSimilar: async function(d) {
      this.isLoading = true;
      this.selected = d;
      this.selectedTag = null;
      this.selectedAuthor = null;
      this.selectedPublisher = null;
      const query = {
        query: {
          script_source: {
            query: { match_all: {} },
            script: {
              source: "cosineSimilarity(params.query_vector, doc['feature_vector']) + 1.0",
              params: { query_vector: d.feature_vector }
            }
          }
        },
        size: 20
      };

      const response = await fetch(searchUrl, {
        method: 'POST',
        headers: {
          "Content-Type": "application/json; charset=utf-8"
        },
        body: JSON.stringify(query)
      });
      const json = await response.json();
      this.list = json.hits.hits.map(doc => doc._source).filter(book => book.id != d.id);
      this.hit = json.hits.total.value;
      this.isLoading = false;
      VueScrollTo.scrollTo("#search-top", 300);
    },
    searchAuthor: async function(author) {
      this.isLoading = true;
      this.selected = null;
      this.selectedtag = null;
      this.selectedAuthor = author;
      this.selectedPublisher = null;
      const query = {
        query: {
          term: {
            responsibility: author
          },
        },
        size: 20
      };

      const response = await fetch(searchUrl, {
        method: 'POST',
        headers: {
          "Content-Type": "application/json; charset=utf-8"
        },
        body: JSON.stringify(query)
      });
      const json = await response.json();
      this.list = json.hits.hits.map(doc => doc._source);
      this.hit = json.hits.total.value;
      this.isLoading = false;
      VueScrollTo.scrollTo("#search-top", 300);
    },
    searchPublisher: async function(publisher) {
      this.isLoading = true;
      this.selected = null;
      this.selectedtag = null;
      this.selectedAuthor = null;
      this.selectedPublisher = publisher;
      const query = {
        query: {
          term: {
            publisher: publisher
          },
        },
        size: 20
      };

      const response = await fetch(searchUrl, {
        method: 'POST',
        headers: {
          "Content-Type": "application/json; charset=utf-8"
        },
        body: JSON.stringify(query)
      });
      const json = await response.json();
      this.list = json.hits.hits.map(doc => doc._source);
      this.hit = json.hits.total.value;
      this.isLoading = false;
      VueScrollTo.scrollTo("#search-top", 300);
    },
    searchTag: async function(tag) {
      this.isLoading = true;
      this.selected = null;
      this.selectedTag = tag;
      this.selectedAuthor = null;
      this.selectedPublisher = null;
      const q = {
        query: {
          term: {
            tags: tag
          }
        },
        size: 20
      };

      const response = await fetch(searchUrl, {
        method: 'POST',
        headers: {
          "Content-Type": "application/json; charset=utf-8"
        },
        body: JSON.stringify(q)
      });
      const json = await response.json();
      this.list = json.hits.hits.map(doc => doc._source);
      this.hit = json.hits.total.value;
      this.isLoading = false;
      VueScrollTo.scrollTo("#search-top", 300);
    }
  }
}
</script>

<style>
.tags {
  margin-bottom: 0;
}
.search-tag {
  cursor: pointer;
}
</style>
