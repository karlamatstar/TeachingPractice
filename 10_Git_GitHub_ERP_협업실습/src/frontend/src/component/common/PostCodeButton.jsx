'use client'

import {useState} from "react";
import CButton from "@/component/common/element/CButton";

// 주소검색 공통
export default function PostCodeButton({onCompletePostData, buttonRender}) {
	const [open, setOpen] = useState(false);
	
	const openPostcode = () => {
		if (!window || window === undefined) return;
		
		const postCode = new window.daum.Postcode({
			oncomplete(data) {
				onCompletePostData?.(data);
			},
		});
		
		postCode.open();
		
	};
	
	return (
		<>
			<CButton
				type="type2"
				buttonName="주소검색"
				onClick={openPostcode}
			/>
		</>
	)
}