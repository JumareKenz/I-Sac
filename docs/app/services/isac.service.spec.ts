import { TestBed } from '@angular/core/testing';

import { IsacService } from './isac.service';

describe('IsacService', () => {
  let service: IsacService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(IsacService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
