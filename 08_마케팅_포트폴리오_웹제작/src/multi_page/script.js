const modal = document.getElementById('projectModal');
const modalTitle = document.getElementById('modalTitle');
const modalBody = document.getElementById('modalBody');
const modalClose = document.getElementById('modalClose');
const filterButtons = document.querySelectorAll('.filter-chip');
const projectCards = document.querySelectorAll('.project-card');
const toast = document.getElementById('toast');
const contactForm = document.getElementById('contactForm');
const formStatus = document.getElementById('formStatus');
const navToggle = document.querySelector('.nav-toggle');
const navLinks = document.querySelector('.nav-links');

const projectDetails = {
  'project-1': {
    title: '광고 성과 개선 캠페인',
    body: '문제 인식: CPA 상승과 유입 품질 저하. 해결 과정: 목표군 세분화, 광고 문구 A/B 테스트, 리타겟팅 흐름 재구성. 결과: ROAS 300% 달성, CPA 18% 절감.'
  },
  'project-2': {
    title: '브랜드 콘텐츠 리뉴얼',
    body: '문제 인식: 콘텐츠 체류 시간이 낮고 전환 연결이 부족함. 해결 과정: 키워드 중심 시리즈 제작과 CTA 배치 개선. 결과: 체류 시간 40% 증가, SEO 클릭률 상승.'
  },
  'project-3': {
    title: 'CRM 리드 리타겟팅',
    body: '문제 인식: 신규 유입은 늘었지만 재방문 전환이 낮음. 해결 과정: 이메일/푸시 시퀀스 설계와 이벤트 기반 발송. 결과: 전환율 50% 개선, 재방문율 상승.'
  }
};

function showToast(message) {
  toast.textContent = message;
  toast.classList.add('show');
  clearTimeout(showToast.timer);
  showToast.timer = setTimeout(() => toast.classList.remove('show'), 2200);
}

function openModal(id) {
  const item = projectDetails[id];
  if (!item) return;
  modalTitle.textContent = item.title;
  modalBody.textContent = item.body;
  modal.classList.add('open');
  modal.setAttribute('aria-hidden', 'false');
}

function closeModal() {
  modal.classList.remove('open');
  modal.setAttribute('aria-hidden', 'true');
}

filterButtons.forEach((button) => {
  button.addEventListener('click', () => {
    const filter = button.dataset.filter;
    filterButtons.forEach((item) => item.classList.remove('active'));
    button.classList.add('active');

    projectCards.forEach((card) => {
      const match = filter === 'all' || card.dataset.category === filter;
      card.style.display = match ? 'block' : 'none';
    });

    showToast(`${button.textContent} 카테고리로 필터링되었습니다.`);
  });
});

projectCards.forEach((card) => {
  card.querySelector('.text-link').addEventListener('click', () => {
    openModal(card.querySelector('.text-link').dataset.modal);
  });
});

modalClose.addEventListener('click', closeModal);
modal.addEventListener('click', (event) => {
  if (event.target === modal) closeModal();
});
window.addEventListener('keydown', (event) => {
  if (event.key === 'Escape') closeModal();
});

contactForm.addEventListener('submit', (event) => {
  event.preventDefault();
  const formData = new FormData(contactForm);
  const name = (formData.get('name') || '').toString().trim();
  const email = (formData.get('email') || '').toString().trim();
  const title = (formData.get('title') || '').toString().trim();
  const message = (formData.get('message') || '').toString().trim();

  if (!name || !email || !title || !message) {
    formStatus.textContent = '필수 항목을 모두 입력해 주세요.';
    showToast('입력값을 다시 확인해 주세요.');
    return;
  }

  const sanitized = {
    name: name.replace(/[<>]/g, ''),
    email: email.replace(/[<>]/g, ''),
    title: title.replace(/[<>]/g, ''),
    message: message.replace(/[<>]/g, '')
  };

  formStatus.textContent = `문의가 접수되었습니다. ${sanitized.name}님께 확인 메일을 보내드릴게요.`;
  contactForm.reset();
  showToast('문의가 정상적으로 접수되었습니다.');
});

navToggle?.addEventListener('click', () => {
  navLinks.classList.toggle('open');
});

navLinks?.querySelectorAll('a').forEach((link) => {
  link.addEventListener('click', () => navLinks.classList.remove('open'));
});

const counters = document.querySelectorAll('.metric-value');
const animateCounters = () => {
  counters.forEach((counter) => {
    const target = Number(counter.dataset.target || 0);
    let current = 0;
    const duration = 1200;
    const step = Math.max(1, Math.floor(duration / target));

    const timer = setInterval(() => {
      current += 1;
      counter.textContent = current.toString();
      if (current >= target) {
        counter.textContent = `${target}${target === 300 ? '%' : ''}${target === 50 ? '%' : ''}`;
        clearInterval(timer);
      }
    }, step);
  });
};

window.addEventListener('load', () => {
  animateCounters();
});

document.getElementById('downloadDemoBtn').addEventListener('click', () => {
  showToast('이력서 다운로드가 준비되었습니다. 실제 배포 시 PDF 파일을 연결해 주세요.');
});
