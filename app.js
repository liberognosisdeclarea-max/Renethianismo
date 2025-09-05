document.addEventListener('DOMContentLoaded', () => {
  const correctPassword = 'Reneth123';

  const loginScreen = document.getElementById('loginScreen');
  const loginBtn = document.getElementById('loginBtn');
  const passwordInput = document.getElementById('password');
  const loginMsg = document.getElementById('loginMsg');

  const app = document.getElementById('app');
  const views = document.querySelectorAll('.view');

  loginBtn.addEventListener('click', () => {
    if (passwordInput.value === correctPassword) {
      loginScreen.classList.add('hidden');
      app.classList.remove('hidden');
      showView('feedView');
    } else {
      loginMsg.textContent = 'Contraseña incorrecta';
    }
  });

  function showView(id) {
    views.forEach(v => v.classList.add('hidden'));
    document.getElementById(id).classList.remove('hidden');
    if (id === 'feedView') renderPosts();
    if (id === 'groupsView') renderGroups();
    if (id === 'membersView') renderMembers();
  }

  document.querySelectorAll('[data-view]').forEach(btn => {
    btn.addEventListener('click', () => showView(btn.dataset.view));
  });

  const encrypt = str => btoa(str);
  const decrypt = str => atob(str);

  let groups = JSON.parse(localStorage.getItem('groups')) || ['Parroquia San Réneth','Sernaztech','Menzttadoh'];
  let members = JSON.parse(localStorage.getItem('members')) || [{name:encrypt('Réneth Oso'),animal:'Oso 🐻'}];
  let posts = JSON.parse(localStorage.getItem('posts')) || [];

  document.getElementById('addGroupBtn').addEventListener('click', () => {
    const input = document.getElementById('newGroupName');
    const name = input.value.trim();
    if (!name) return;
    groups.push(name);
    input.value = '';
    renderGroups();
  });

  function renderGroups() {
    const list = document.getElementById('groupsList');
    list.innerHTML = '';
    groups.forEach(g => {
      const li = document.createElement('li');
      li.textContent = g;
      li.className = 'post';
      list.appendChild(li);
    });
    localStorage.setItem('groups', JSON.stringify(groups));
  }

  document.getElementById('addMemberBtn').addEventListener('click', () => {
    const name = document.getElementById('newMemberName').value.trim();
    const animal = document.getElementById('newMemberAnimal').value;
    if (!name) return;
    members.push({name: encrypt(name), animal});
    document.getElementById('newMemberName').value = '';
    renderMembers();
  });

  function renderMembers() {
    const container = document.getElementById('membersContainer');
    container.innerHTML = '';
    members.forEach(m => {
      const card = document.createElement('div');
      card.textContent = `${decrypt(m.name)} (${m.animal})`;
      container.appendChild(card);
    });
    localStorage.setItem('members', JSON.stringify(members));
  }

  let mediaRecorder;
  let audioChunks = [];

  document.getElementById('startRec').addEventListener('click', () => {
    if (!navigator.mediaDevices) {
      alert('No soporta grabación.');
      return;
    }
    navigator.mediaDevices.getUserMedia({audio:true}).then(stream => {
      mediaRecorder = new MediaRecorder(stream);
      audioChunks = [];
      mediaRecorder.start();
      document.getElementById('recordingStatus').textContent = '🎙️ Grabando...';
      mediaRecorder.ondataavailable = e => audioChunks.push(e.data);
    });
  });

  document.getElementById('stopRec').addEventListener('click', () => {
    if (!mediaRecorder) return;
    mediaRecorder.stop();
    mediaRecorder.onstop = () => {
      document.getElementById('recordingStatus').textContent = '✅ Grabación lista';
    };
  });

  document.getElementById('publishBtn').addEventListener('click', addPost);

  function addPost() {
    const content = document.getElementById('postContent').value.trim();
    const imageFile = document.getElementById('postImage').files[0];
    if (!content && !imageFile && audioChunks.length === 0) return;

    const post = {author: encrypt('Réneth Oso'), content: encrypt(content), date: new Date().toLocaleString(), reactions:{}, replies:[], image:'', audio:''};

    if (imageFile) {
      const reader = new FileReader();
      reader.onload = e => {
        post.image = e.target.result;
        if (audioChunks.length > 0) saveAudio(post); else savePost(post);
      };
      reader.readAsDataURL(imageFile);
    } else if (audioChunks.length > 0) {
      saveAudio(post);
    } else {
      savePost(post);
    }
  }

  function saveAudio(post) {
    const blob = new Blob(audioChunks, {type:'audio/webm'});
    post.audio = URL.createObjectURL(blob);
    audioChunks = [];
    savePost(post);
  }

  function savePost(post) {
    posts.unshift(post);
    localStorage.setItem('posts', JSON.stringify(posts));
    document.getElementById('postContent').value = '';
    document.getElementById('postImage').value = '';
    document.getElementById('recordingStatus').textContent = '';
    renderPosts();
  }

  function renderPosts() {
    const container = document.getElementById('postsContainer');
    container.innerHTML = '';
    posts.forEach((p, index) => {
      const card = document.createElement('div');
      card.className = 'post';
      let html = `<p><strong>${p.author ? decrypt(p.author) : ''}</strong> <small>${p.date}</small></p>`;
      if (p.content) html += `<p>${decrypt(p.content)}</p>`;
      if (p.image) html += `<img src="${p.image}" alt="post">`;
      if (p.audio) html += `<audio controls src="${p.audio}"></audio>`;
      html += `
        <div class="buttons">
          <span data-react="🔥">🔥 ${p.reactions['🔥'] || ''}</span>
          <span data-react="🐻">🐻 ${p.reactions['🐻'] || ''}</span>
          <span data-react="🌿">🌿 ${p.reactions['🌿'] || ''}</span>
        </div>
        <button class="delete-btn">Eliminar</button>
        <div class="reply-box">
          <input type="text" placeholder="Responder...">
          <button class="reply-btn">Enviar</button>
        </div>
      `;
      card.innerHTML = html;
      container.appendChild(card);

      card.querySelectorAll('[data-react]').forEach(btn => {
        btn.addEventListener('click', () => toggleReaction(index, btn.dataset.react));
      });

      card.querySelector('.delete-btn').addEventListener('click', () => {
        posts.splice(index,1);
        localStorage.setItem('posts', JSON.stringify(posts));
        renderPosts();
      });

      const replyInput = card.querySelector('input');
      card.querySelector('.reply-btn').addEventListener('click', () => {
        const text = replyInput.value.trim();
        if (!text) return;
        posts[index].replies.push({author: encrypt('Réneth Oso'), content: encrypt(text), date:new Date().toLocaleString()});
        localStorage.setItem('posts', JSON.stringify(posts));
        renderPosts();
      });

      const repliesContainer = document.createElement('div');
      p.replies.forEach(r => {
        const div = document.createElement('div');
        div.className = 'reply';
        div.innerHTML = `<strong>${decrypt(r.author)}</strong>: ${decrypt(r.content)} <small>${r.date}</small>`;
        repliesContainer.appendChild(div);
      });
      card.appendChild(repliesContainer);
    });
  }

  function toggleReaction(index, reaction) {
    const post = posts[index];
    if (post.reactions[reaction]) delete post.reactions[reaction];
    else post.reactions[reaction] = '1';
    localStorage.setItem('posts', JSON.stringify(posts));
    renderPosts();
  }

  const ghostUsers = [encrypt('Zorra Astuta'),encrypt('Gato Místico'),encrypt('Oso Sabio')];
  const ghostPhrases = [
    "La presencia no se pide, se toma 🔥",
    "Cada pensamiento es un mundo 🌿",
    "El fuego interno nunca se apaga 🐻",
    "Ser auténtico es ser libre 💯",
    "La energía habla más fuerte que las palabras",
    "Donde hay calma, hay poder",
    "Tu sombra también tiene voz"
  ];

  function ghostAutoPost() {
    const user = ghostUsers[Math.floor(Math.random()*ghostUsers.length)];
    const phrase = ghostPhrases[Math.floor(Math.random()*ghostPhrases.length)];
    const post = {author:user, content:encrypt(phrase), date:new Date().toLocaleString(), reactions:{}, replies:[]};
    posts.unshift(post);
    localStorage.setItem('posts', JSON.stringify(posts));
    renderPosts();
  }

  setInterval(() => ghostAutoPost(), Math.floor(Math.random()*20000)+20000);
});
