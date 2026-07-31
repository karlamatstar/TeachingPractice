package com.logitics.erp.common.init;

import com.logitics.erp.department.entity.Department;
import com.logitics.erp.department.repository.DepartmentRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
public class InitDepartmentData implements CommandLineRunner {

	private final DepartmentRepository departmentRepository;

	@Override
	public void run(String... args) {

		if (departmentRepository.count() > 0) {
			return;
		}

		Department management = departmentRepository.save(
						new Department("경영지원본부", null)
		);

		departmentRepository.save(new Department("인사팀", management));
		departmentRepository.save(new Department("재무회계팀", management));
		departmentRepository.save(new Department("총무팀", management));

		Department logistics = departmentRepository.save(
						new Department("물류운영본부", null)
		);

		departmentRepository.save(new Department("배차팀", logistics));
		departmentRepository.save(new Department("배송운영팀", logistics));
		departmentRepository.save(new Department("배송관리팀", logistics));
		departmentRepository.save(new Department("관제팀", logistics));
		departmentRepository.save(new Department("긴급배송팀", logistics));

		Department cold = departmentRepository.save(
						new Department("냉장/냉동물류본부", null)
		);

		departmentRepository.save(new Department("냉장물류팀", cold));
		departmentRepository.save(new Department("냉동물류팀", cold));
		departmentRepository.save(new Department("신선식품배송팀", cold));
		departmentRepository.save(new Department("새벽배송팀", cold));

		Department vehicle = departmentRepository.save(
						new Department("차량관리본부", null)
		);

		departmentRepository.save(new Department("차량정비팀", vehicle));
		departmentRepository.save(new Department("차량관제팀", vehicle));
		departmentRepository.save(new Department("유류관리팀", vehicle));
		departmentRepository.save(new Department("기사관리팀", vehicle));

		Department warehouse = departmentRepository.save(
						new Department("창고운영본부", null)
		);

		departmentRepository.save(new Department("입고팀", warehouse));
		departmentRepository.save(new Department("출고팀", warehouse));
		departmentRepository.save(new Department("재고관리팀", warehouse));
		departmentRepository.save(new Department("냉장창고팀", warehouse));
		departmentRepository.save(new Department("냉동창고팀", warehouse));

		Department sales = departmentRepository.save(
						new Department("영업본부", null)
		);

		departmentRepository.save(new Department("물류영업팀", sales));
		departmentRepository.save(new Department("거래처관리팀", sales));
		departmentRepository.save(new Department("고객지원팀(CS)", sales));

		Department it = departmentRepository.save(
						new Department("IT본부", null)
		);

		departmentRepository.save(new Department("ERP개발팀", it));
		departmentRepository.save(new Department("인프라운영팀", it));
		departmentRepository.save(new Department("보안관리팀", it));

	}
}