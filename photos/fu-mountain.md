---
layout: gallery
title: "福山步道"
permalink: /photos/fu-mountain/
lang: "zh-TW"
---

<style>
.gallery-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
  margin-top: 2rem;
}

.gallery-item {
  position: relative;
  overflow: hidden;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  transition: transform 0.2s;
}

.gallery-item:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 16px rgba(0,0,0,0.2);
}

.gallery-item img {
  width: 100%;
  height: auto;
  display: block;
}

.gallery-item-info {
  padding: 0.5rem;
  background: #f5f5f5;
}

.gallery-item-title {
  font-size: 0.9rem;
  font-weight: 500;
  margin: 0;
  color: #333;
}

.gallery-item-date {
  font-size: 0.8rem;
  color: #666;
  margin: 0.25rem 0 0 0;
}
</style>

<div id="gallery-container">
  <p>載入相簿中...</p>
</div>

<script>
(function() {
  const albumId = 'fu-mountain';
  const jsonPath = '/data/photos/by-album.json';
  
  fetch(jsonPath)
    .then(response => response.json())
    .then(data => {
      const album = data.albums.find(a => a.id === albumId);
      
      if (!album) {
        document.getElementById('gallery-container').innerHTML = '<p>找不到相簿資料</p>';
        return;
      }
      
      let html = '<div class="gallery-grid">';
      
      album.photos.forEach(photo => {
        html += `
          <div class="gallery-item">
            <a href="/${photo.path}" target="_blank">
              <img src="/${photo.thumbnail}" alt="${photo.title}" loading="lazy">
            </a>
            <div class="gallery-item-info">
              <p class="gallery-item-title">${photo.title}</p>
              ${photo.date ? `<p class="gallery-item-date">${photo.date}</p>` : ''}
            </div>
          </div>
        `;
      });
      
      html += '</div>';
      
      document.getElementById('gallery-container').innerHTML = html;
    })
    .catch(error => {
      console.error('Error loading album data:', error);
      document.getElementById('gallery-container').innerHTML = '<p>載入相簿資料時發生錯誤</p>';
    });
})();
</script>
