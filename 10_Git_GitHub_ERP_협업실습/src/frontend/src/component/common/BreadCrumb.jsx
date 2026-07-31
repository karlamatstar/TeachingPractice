import s from './BreadCrumb.module.css'
const breadcrumbList = [
	{ type: 'icon', path: '/breadcrumb/breadcrumb-home.png', title: '' },
	{ type: 'title', path: '/breadcrumb/breadcrumb-home.png', title: '인사관리' },
	{ type: 'title', path: '/breadcrumb/breadcrumb-home.png', title: '인사정보' },
	{ type: 'title', path: '/breadcrumb/breadcrumb-home.png', title: '인사정보등록' },
];

export default function BreadCrumb({ crumList = breadcrumbList }) {

	const dummy = {
		iconPath: '/breadcrumb/breadcrumb-home.png',
		depth1: '인사관리',
		depth2: '인사정보',
		depth3: '인사정보등록',
	}


	const renderBreadCrumb = (item, idx) => {
		const renderList = [];

		switch (item.type) {
			case 'icon':
				renderList.push(<img key={`icon ${idx}`} className='w-[9px] h-[9px]' src={item.path} />)
				break;
			case 'title':
				renderList.push(<span key={`title ${idx}`}>{item.title}</span>)
				break;
		}

		if (crumList.length - 1 !== idx) {
			renderList.push(<img key={`breadcrumb${idx}`} className='w-[12px] h-[12px]' src="/breadcrumb/arrowRight.png"
				alt="" />);
		}

		return (
			renderList
		);
	}

	return (
		<div className={s.container}>
			{crumList.map(renderBreadCrumb)}
		</div>
	)

}