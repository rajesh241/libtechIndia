import { AfterViewInit, Component, OnInit, ViewChild } from '@angular/core';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { MatTable } from '@angular/material/table';
import { UserListDataSource, UserListItem } from './user-list-datasource';

@Component({
  selector: 'user-list',
  templateUrl: './user-list.component.html',
  styleUrls: ['./user-list.component.scss']
})
export class UserListComponent implements AfterViewInit, OnInit {
  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort) sort: MatSort;
  @ViewChild(MatTable) table: MatTable<UserListItem>;
  dataSource: UserListDataSource;

  /** Columns displayed in the table. Columns IDs can be added, removed, or reordered. */
  displayedColumns = ['id', 'name'];

  ngOnInit() {
    console.log(`UserListComponent.ngOnInit()`);
    this.dataSource = new UserListDataSource();
  }

  ngAfterViewInit() {
    console.log(`UserListComponent.ngAfterViewInit()`);
    this.dataSource.sort = this.sort;
    this.dataSource.paginator = this.paginator;
    this.table.dataSource = this.dataSource;
  }

  rowClicked(row) {
    console.log(`UserListComponent.rowClicked(${row})`, row);
  }

  universalFilter(filterValue: string) {
    console.log(`UserListComponent.universalFilter(${filterValue})`);
    // MatDataSource has filter FIXME - this.dataSource.filter = filterValue.trim().toLowerCase();
  }
}
